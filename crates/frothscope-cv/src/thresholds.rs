use crate::image::Image;
use crate::Metrics;
use crate::{Areas, Region, BINARY_RANGE, CONTRAST_RANGE, INV_BINARY_RANGE};
use opencv::core;
use rayon::prelude::*;

#[derive(Debug, Clone, Copy)]
pub struct Count {
    pub threshold: i32,
    pub glares: usize,
}

pub type Pairs = Vec<Count>;

#[derive(Debug, Clone, Copy, Default)]
pub struct Thresholds<T> {
    pub binary: T,
    pub contrast: T,
    pub inv_binary: T,
}

pub type Required = Thresholds<Option<i32>>;

impl Image<'_> {
    fn count_glares(&self, binary: i32, inv_binary: i32) -> opencv::Result<usize> {
        let mask = self.get_full_mask(binary, inv_binary)?;
        Ok(Metrics::get_contours(&mask, self.areas)?.len())
    }

    fn get_binary_threshold(&self) -> opencv::Result<(i32, Pairs)> {
        find_best_threshold(BINARY_RANGE, |binary| self.count_glares(binary, 0))
    }

    fn get_contrast_threshold(&self, binary: i32) -> opencv::Result<(i32, Pairs)> {
        find_best_threshold(CONTRAST_RANGE, |contrast| {
            self.get_contrasted_img(contrast)?.count_glares(binary, 0)
        })
    }

    fn get_inv_binary_threshold(&self, binary: i32) -> opencv::Result<(i32, Pairs)> {
        find_best_threshold(INV_BINARY_RANGE, |inv_binary| self.count_glares(binary, inv_binary))
    }
}

fn find_best_threshold(
    range: std::ops::Range<i32>,
    count_glares: impl Fn(i32) -> opencv::Result<usize> + Sync,
) -> opencv::Result<(i32, Pairs)> {
    let pairs = range
        .into_par_iter()
        .map(|threshold| {
            Ok(Count {
                threshold,
                glares: count_glares(threshold)?,
            })
        })
        .collect::<opencv::Result<Pairs>>()?;

    let best = pairs
        .iter()
        .max_by_key(|count| count.glares)
        .map(|count| count.threshold)
        .expect("threshold range is empty");

    Ok((best, pairs))
}

pub fn get_thresholds(
    frame: &core::Mat,
    region: &Region,
    areas: Areas,
    required: Required,
) -> opencv::Result<(Thresholds<i32>, Thresholds<Pairs>)> {
    let img = region.get_image(frame, areas)?;
    let mut thresholds = Thresholds::default();
    let mut pairs = Thresholds::default();

    let probe = match required.binary {
        Some(value) => value,
        None => img.get_binary_threshold()?.0,
    };

    (thresholds.contrast, pairs.contrast) = match required.contrast {
        Some(value) => (value, Pairs::new()),
        None => img.get_contrast_threshold(probe)?,
    };

    let contrasted = img.get_contrasted_img(thresholds.contrast)?;

    (thresholds.binary, pairs.binary) = match required.binary {
        Some(value) => (value, Pairs::new()),
        None => contrasted.get_binary_threshold()?,
    };

    (thresholds.inv_binary, pairs.inv_binary) = match required.inv_binary {
        Some(value) => (value, Pairs::new()),
        None => contrasted.get_inv_binary_threshold(thresholds.binary)?,
    };

    Ok((thresholds, pairs))
}
