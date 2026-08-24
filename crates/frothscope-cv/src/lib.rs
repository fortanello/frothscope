use opencv::core;

mod clahe;
mod image;
mod metrics;
mod region;
mod thresholds;

pub use metrics::Metrics;
pub use region::Region;
pub use thresholds::{get_thresholds, Count, Pairs, Required, Thresholds};

pub const NO_CONTRAST: i32 = 0;

pub const CONTRAST_RANGE: std::ops::Range<i32> = 0..5;
pub const BINARY_RANGE: std::ops::Range<i32> = 80..245;
pub const INV_BINARY_RANGE: std::ops::Range<i32> = 0..120;

#[derive(Debug, Clone, Copy)]
pub struct Areas {
    pub min: f64,
    pub max: f64,
}

pub fn get_result(
    frame: &core::Mat,
    region: &Region,
    areas: Areas,
    thresholds: &Thresholds<i32>,
) -> opencv::Result<(Metrics, core::Mat)> {
    let img = region
        .get_image(frame, areas)?
        .get_contrasted_img(thresholds.contrast)?;
    let mask = img.get_full_mask(thresholds.binary, thresholds.inv_binary)?;
    let contours = Metrics::get_contours(&mask, areas)?;

    Ok((
        Metrics::new(&contours, img.get_area()?)?,
        img.get_marked_img(&contours)?,
    ))
}
