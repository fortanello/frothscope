use crate::image::Image;
use crate::Areas;
use opencv::{core, imgproc, prelude::*};

pub enum Region {
    Whole,
    Polygon { rect: core::Rect, mask: core::Mat },
}

impl Region {
    pub fn polygon(points: &[(i32, i32)]) -> opencv::Result<Self> {
        let x0 = points.iter().map(|p| p.0).min().unwrap();
        let y0 = points.iter().map(|p| p.1).min().unwrap();
        let x1 = points.iter().map(|p| p.0).max().unwrap();
        let y1 = points.iter().map(|p| p.1).max().unwrap();
        let rect = core::Rect::new(x0, y0, x1 - x0 + 1, y1 - y0 + 1);

        let shifted: core::Vector<core::Point> = points
            .iter()
            .map(|&(x, y)| core::Point::new(x - x0, y - y0))
            .collect();
        let mut mask = core::Mat::zeros_size(rect.size(), core::CV_8UC1)?.to_mat()?;
        imgproc::fill_poly_def(
            &mut mask,
            &core::Vector::<core::Vector<core::Point>>::from_iter([shifted]),
            core::Scalar::all(255.0),
        )?;

        Ok(Self::Polygon { rect, mask })
    }

    pub(crate) fn get_image(&self, frame: &core::Mat, areas: Areas) -> opencv::Result<Image<'_>> {
        match self {
            Self::Whole => Image::new(frame.try_clone()?, None, areas),
            Self::Polygon { rect, mask } => {
                Image::new(core::Mat::roi(frame, *rect)?.try_clone()?, Some(mask), areas)
            }
        }
    }
}
