use crate::metrics::Contours;
use crate::{clahe, Areas, NO_CONTRAST};
use opencv::{core, imgproc, prelude::*};

pub(crate) struct Image<'a> {
    bgr: core::Mat,
    gray: core::Mat,
    mask: Option<&'a core::Mat>,
    pub(crate) areas: Areas,
}

impl<'a> Image<'a> {
    pub(crate) fn new(
        bgr: core::Mat,
        mask: Option<&'a core::Mat>,
        areas: Areas,
    ) -> opencv::Result<Self> {
        let mut gray = core::Mat::default();
        imgproc::cvt_color_def(&bgr, &mut gray, imgproc::COLOR_BGR2GRAY)?;

        Ok(Self {
            bgr,
            gray,
            mask,
            areas,
        })
    }

    pub(crate) fn get_area(&self) -> opencv::Result<f64> {
        Ok(match self.mask {
            Some(mask) => core::count_non_zero(mask)? as f64,
            None => (self.gray.rows() as f64) * (self.gray.cols() as f64),
        })
    }

    pub(crate) fn get_contrasted_img(&self, contrast: i32) -> opencv::Result<Self> {
        if contrast == NO_CONTRAST {
            return Self::new(self.bgr.clone(), self.mask, self.areas);
        }

        let mut lab = core::Mat::default();
        imgproc::cvt_color_def(&self.bgr, &mut lab, imgproc::COLOR_BGR2Lab)?;

        let mut lightness = core::Mat::default();
        core::extract_channel(&lab, &mut lightness, 0)?;

        let equalized =
            clahe::equalize(&lightness, self.mask, contrast as f64, clahe::Tiles::default())?;
        core::insert_channel(&equalized, &mut lab, 0)?;

        let mut bgr = core::Mat::default();
        imgproc::cvt_color_def(&lab, &mut bgr, imgproc::COLOR_Lab2BGR)?;
        Self::new(bgr, self.mask, self.areas)
    }

    fn get_resized_img(&self, img: &core::Mat) -> opencv::Result<core::Mat> {
        match self.mask {
            Some(mask) => {
                let mut out = core::Mat::default();
                core::bitwise_and(img, img, &mut out, mask)?;
                Ok(out)
            }
            None => Ok(img.clone()),
        }
    }

    fn get_inv_mask(&self, inv_binary: i32) -> opencv::Result<core::Mat> {
        let mut dark = core::Mat::default();
        imgproc::threshold(
            &self.gray,
            &mut dark,
            inv_binary as f64,
            255.0,
            imgproc::THRESH_BINARY_INV,
        )?;

        let mut contours = Contours::new();
        imgproc::find_contours_def(
            &dark,
            &mut contours,
            imgproc::RETR_EXTERNAL,
            imgproc::CHAIN_APPROX_SIMPLE,
        )?;

        let mut inv_glares = core::Mat::zeros_size(self.gray.size()?, core::CV_8UC1)?.to_mat()?;
        for (i, contour) in contours.iter().enumerate() {
            let area = imgproc::contour_area_def(&contour)?;
            if area > self.areas.min && area < self.areas.max {
                imgproc::draw_contours(
                    &mut inv_glares,
                    &contours,
                    i as i32,
                    core::Scalar::all(255.0),
                    -1,
                    imgproc::LINE_8,
                    &core::no_array(),
                    0,
                    core::Point::new(0, 0),
                )?;
            }
        }

        Ok(inv_glares)
    }

    fn get_bright_mask(&self, binary: i32) -> opencv::Result<core::Mat> {
        let mut bright = core::Mat::default();
        imgproc::threshold(
            &self.gray,
            &mut bright,
            binary as f64,
            255.0,
            imgproc::THRESH_BINARY,
        )?;
        Ok(bright)
    }

    pub(crate) fn get_full_mask(&self, binary: i32, inv_binary: i32) -> opencv::Result<core::Mat> {
        let mut full = core::Mat::default();
        core::bitwise_or(
            &self.get_bright_mask(binary)?,
            &self.get_inv_mask(inv_binary)?,
            &mut full,
            &core::no_array(),
        )?;

        self.get_resized_img(&full)
    }

    pub(crate) fn get_marked_img(&self, contours: &Contours) -> opencv::Result<core::Mat> {
        let mut marked = core::Mat::default();
        imgproc::cvt_color_def(&self.bgr, &mut marked, imgproc::COLOR_BGR2BGRA)?;
        if let Some(outline) = self.mask {
            core::insert_channel(outline, &mut marked, 3)?;
        }

        imgproc::draw_contours_def(
            &mut marked,
            contours,
            -1,
            core::Scalar::new(0.0, 255.0, 0.0, 255.0),
        )?;
        Ok(marked)
    }
}
