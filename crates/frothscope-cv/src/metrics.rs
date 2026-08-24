use crate::Areas;
use opencv::{core, imgproc};

pub(crate) type Contours = core::Vector<core::Vector<core::Point>>;

pub struct Metrics {
    area: f64,
    count: usize,
    distances: Vec<f64>,
}

impl Metrics {
    pub(crate) fn get_contours(glares: &core::Mat, areas: Areas) -> opencv::Result<Contours> {
        let mut found = Contours::new();
        imgproc::find_contours_def(
            glares,
            &mut found,
            imgproc::RETR_EXTERNAL,
            imgproc::CHAIN_APPROX_SIMPLE,
        )?;

        let mut kept = Contours::new();
        for contour in found.iter() {
            let area = imgproc::contour_area_def(&contour)?;
            if area > areas.min && area < areas.max {
                kept.push(contour);
            }
        }

        Ok(kept)
    }

    pub(crate) fn new(contours: &Contours, area: f64) -> opencv::Result<Self> {
        let centers = Self::get_centers(contours)?;
        let mut distances = Self::get_distances(&centers);
        distances.sort_by(|a, b| a.partial_cmp(b).unwrap());

        Ok(Self {
            area,
            count: centers.len(),
            distances,
        })
    }

    pub fn area(&self) -> f64 {
        self.area
    }

    pub fn count(&self) -> usize {
        self.count
    }

    pub fn mean(&self) -> Option<f64> {
        if self.distances.is_empty() {
            return None;
        }

        Some(self.distances.iter().sum::<f64>() / self.distances.len() as f64)
    }

    pub fn median(&self) -> Option<f64> {
        if self.distances.is_empty() {
            return None;
        }

        let mid = self.distances.len() / 2;
        Some(if self.distances.len().is_multiple_of(2) {
            (self.distances[mid - 1] + self.distances[mid]) / 2.0
        } else {
            self.distances[mid]
        })
    }

    fn get_centers(contours: &Contours) -> opencv::Result<Vec<core::Point2f>> {
        contours
            .iter()
            .map(|contour| {
                let m = imgproc::moments_def(&contour)?;
                Ok(core::Point2f::new(
                    (m.m10 / m.m00) as f32,
                    (m.m01 / m.m00) as f32,
                ))
            })
            .collect()
    }

    fn get_distances(centers: &[core::Point2f]) -> Vec<f64> {
        let mut nearest = Vec::with_capacity(centers.len());
        for (i, a) in centers.iter().enumerate() {
            let mut best = f64::INFINITY;
            for (j, b) in centers.iter().enumerate() {
                if i == j {
                    continue;
                }

                let dx = (a.x - b.x) as f64;
                let dy = (a.y - b.y) as f64;
                best = best.min(dx * dx + dy * dy);
            }

            if best.is_finite() {
                nearest.push(best.sqrt());
            }
        }

        nearest
    }
}
