use opencv::{core, prelude::*};

const BINS: usize = 256;

pub struct Tiles {
    pub x: usize,
    pub y: usize,
}

impl Default for Tiles {
    fn default() -> Self {
        Self { x: 8, y: 8 }
    }
}

struct Histogram {
    bins: [u32; BINS],
    total: u32,
}

impl Histogram {
    fn new() -> Self {
        Self {
            bins: [0; BINS],
            total: 0,
        }
    }

    fn add(&mut self, value: u8) {
        self.bins[value as usize] += 1;
        self.total += 1;
    }

    fn merge(&mut self, other: &Histogram) {
        for i in 0..BINS {
            self.bins[i] += other.bins[i];
        }
        self.total += other.total;
    }

    fn clip(&self, limit: f64) -> [u32; BINS] {
        if self.total == 0 {
            return [0; BINS];
        }

        let ceiling = (limit * self.total as f64 / BINS as f64).max(1.0) as u32;
        let mut bins = self.bins;
        let mut excess = 0u32;
        for bin in bins.iter_mut() {
            if *bin > ceiling {
                excess += *bin - ceiling;
                *bin = ceiling;
            }
        }

        let share = excess / BINS as u32;
        let remainder = excess % BINS as u32;
        for (i, bin) in bins.iter_mut().enumerate() {
            *bin += share + if (i as u32) < remainder { 1 } else { 0 };
        }
        bins
    }

    fn mapping(&self, limit: f64) -> [u8; BINS] {
        let mut map = [0u8; BINS];
        if self.total == 0 {
            for (i, m) in map.iter_mut().enumerate() {
                *m = i as u8;
            }
            return map;
        }

        let bins = self.clip(limit);
        let total: u32 = bins.iter().sum();
        let mut running = 0u32;
        for (i, m) in map.iter_mut().enumerate() {
            running += bins[i];
            *m = ((running as f64 / total as f64) * 255.0).round() as u8;
        }
        map
    }
}

pub fn equalize(
    gray: &core::Mat,
    mask: Option<&core::Mat>,
    limit: f64,
    tiles: Tiles,
) -> opencv::Result<core::Mat> {
    let rows = gray.rows() as usize;
    let cols = gray.cols() as usize;
    let tile_h = rows.div_ceil(tiles.y).max(1);
    let tile_w = cols.div_ceil(tiles.x).max(1);

    let mut histograms: Vec<Histogram> = (0..tiles.x * tiles.y).map(|_| Histogram::new()).collect();
    let mut overall = Histogram::new();

    for y in 0..rows {
        let row = gray.at_row::<u8>(y as i32)?;
        let mask_row = match mask {
            Some(m) => Some(m.at_row::<u8>(y as i32)?),
            None => None,
        };
        let ty = (y / tile_h).min(tiles.y - 1);

        for x in 0..cols {
            if let Some(mask_row) = mask_row
                && mask_row[x] == 0
            {
                continue;
            }
            let tx = (x / tile_w).min(tiles.x - 1);
            histograms[ty * tiles.x + tx].add(row[x]);
        }
    }

    for histogram in &histograms {
        overall.merge(histogram);
    }

    let fallback = overall.mapping(limit);
    let maps: Vec<[u8; BINS]> = histograms
        .iter()
        .map(|h| if h.total < 16 { fallback } else { h.mapping(limit) })
        .collect();

    let mut out = vec![0u8; rows * cols];
    for y in 0..rows {
        let row = gray.at_row::<u8>(y as i32)?;

        let fy = (y as f64 + 0.5) / tile_h as f64 - 0.5;
        let ty0 = fy.floor().max(0.0) as usize;
        let ty1 = (ty0 + 1).min(tiles.y - 1);
        let wy = (fy - ty0 as f64).clamp(0.0, 1.0);

        for x in 0..cols {
            let fx = (x as f64 + 0.5) / tile_w as f64 - 0.5;
            let tx0 = fx.floor().max(0.0) as usize;
            let tx1 = (tx0 + 1).min(tiles.x - 1);
            let wx = (fx - tx0 as f64).clamp(0.0, 1.0);

            let value = row[x] as usize;
            let at = |ty: usize, tx: usize| maps[ty * tiles.x + tx][value] as f64;

            let blended = at(ty0, tx0) * (1.0 - wx) * (1.0 - wy)
                + at(ty0, tx1) * wx * (1.0 - wy)
                + at(ty1, tx0) * (1.0 - wx) * wy
                + at(ty1, tx1) * wx * wy;

            out[y * cols + x] = blended.round().clamp(0.0, 255.0) as u8;
        }
    }

    core::Mat::new_rows_cols_with_data(rows as i32, cols as i32, &out)?.try_clone()
}
