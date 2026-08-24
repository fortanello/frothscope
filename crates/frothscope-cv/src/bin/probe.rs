use frothscope_cv::{get_result, get_thresholds, Areas, Pairs, Region, Required};
use opencv::{core, imgcodecs, prelude::*, videoio};

struct Cfg {
    source: &'static str,
    frame: u64,
    roi: Option<&'static [(i32, i32)]>,
    required: Required,
    areas: Areas,
}

const CFG: Cfg = Cfg {
    source: "data/froth.jpg",
    frame: 0,
    roi: None,
    required: Required {
        binary: None,
        contrast: None,
        inv_binary: None,
    },
    areas: Areas {
        min: 400.0,
        max: 2000.0,
    },
};

fn load(cfg: &Cfg) -> anyhow::Result<core::Mat> {
    let image = imgcodecs::imread_def(cfg.source)?;
    if !image.empty() {
        return Ok(image);
    }

    let mut cap = videoio::VideoCapture::from_file_def(cfg.source)?;
    anyhow::ensure!(cap.is_opened()?, "cannot open {}", cfg.source);

    for i in 0..cfg.frame {
        anyhow::ensure!(cap.grab()?, "video ended at frame {i}");
    }

    let mut frame = core::Mat::default();
    anyhow::ensure!(
        cap.read(&mut frame)? && !frame.empty(),
        "cannot read frame {}",
        cfg.frame
    );
    Ok(frame)
}

fn write_pairs(path: &str, header: &str, pairs: &Pairs) -> anyhow::Result<()> {
    let mut text = format!("{header},glares\n");
    for count in pairs {
        text.push_str(&format!("{},{}\n", count.threshold, count.glares));
    }
    std::fs::write(path, text)?;
    Ok(())
}

fn main() -> anyhow::Result<()> {
    std::fs::create_dir_all("out")?;
    let frame = load(&CFG)?;
    let size = frame.size()?;

    let region = match CFG.roi {
        Some(points) => Region::polygon(points)?,
        None => Region::Whole,
    };

    println!(
        "кадр:    {} из {} ({}x{})",
        CFG.frame, CFG.source, size.width, size.height
    );

    let started = std::time::Instant::now();
    let (thresholds, pairs) = get_thresholds(&frame, &region, CFG.areas, CFG.required)?;
    println!(
        "пороги:  бинаризация {} контраст {} инверсная {}   за {:.1} c",
        thresholds.binary,
        thresholds.contrast,
        thresholds.inv_binary,
        started.elapsed().as_secs_f64()
    );

    let (metrics, marked) = get_result(&frame, &region, CFG.areas, &thresholds)?;

    println!();
    println!("{:<22}{:.0} px²", "площадь области:", metrics.area());
    print!(
        "{:<22}{:<6}{:>7.2} на 1000 px²",
        "бликов:",
        metrics.count(),
        metrics.count() as f64 / metrics.area() * 1000.0
    );
    match (metrics.mean(), metrics.median()) {
        (Some(mean), Some(median)) => {
            println!("   до соседа ср./мед. {mean:.1} / {median:.1}")
        }
        _ => println!(),
    }

    let prefix = format!("out/{:03}", CFG.frame);
    imgcodecs::imwrite_def(format!("{prefix}-glares.png"), &marked)?;
    write_pairs(&format!("{prefix}-pairs-binary.csv"), "binary", &pairs.binary)?;
    write_pairs(
        &format!("{prefix}-pairs-contrast.csv"),
        "contrast",
        &pairs.contrast,
    )?;
    write_pairs(
        &format!("{prefix}-pairs-inv.csv"),
        "inv_binary",
        &pairs.inv_binary,
    )?;
    println!("\nкартинка и пары: {prefix}-*");
    Ok(())
}
