use rand::{thread_rng, Rng};
use sha2::{Digest, Sha256};
use std::sync::{Arc, RwLock};
use tokio::time::Instant;

pub fn generate_nonce(length: usize) -> String {
    let charset = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let mut rng = thread_rng();
    let result: String = (0..length)
        .map(|_| {
            let idx = rng.gen_range(0..charset.len());
            charset[idx] as char
        })
        .collect();
    result
}

pub fn generate_hash(data: &str) -> String {
    let hash = Sha256::digest(data);
    format!("{:x}", hash)
}

pub async fn find_hash(mission_hash: &str, require: &str, cores: u8) -> (String, String) {
    let core_ids = core_affinity::get_core_ids().unwrap();
    let global_match_nonce = Arc::new(RwLock::new("".to_string()));

    let handles = core_ids
        .into_iter()
        .map(|i| {
            let global_match_nonce = Arc::clone(&global_match_nonce);

            std::thread::spawn({
                let mission_hash = mission_hash.to_owned().clone();
                let require = require.to_owned().clone();
                move || {
                    // Return if core should not be used
                    if (i.id as u8).ge(&cores) {
                        return (String::from(""), String::from(""));
                    }

                    // Pin to core
                    let _ = core_affinity::set_for_current(i);

                    // Start hashing
                    #[cfg(debug_assertions)]
                    let timer = Instant::now();

                    loop {
                        // Create hash
                        let nonce = generate_nonce(48);
                        let str = format!("{}{}", mission_hash, nonce);
                        let best_match = generate_hash(&str);

                        // Check if hash is valid
                        if best_match.starts_with(&require) {
                            #[cfg(debug_assertions)]
                            println!(
                                "Hash found: {} ({}s)\nNonce: {}",
                                best_match,
                                timer.elapsed().as_secs_f64(),
                                nonce
                            );

                            let copy_best_match_nonce = nonce.clone();
                            *global_match_nonce.write().unwrap() = copy_best_match_nonce;
                            return (nonce, best_match);
                        }

                        let global_match_hash = global_match_nonce.read().unwrap().clone();
                        if global_match_hash != "" {
                            break;
                        }
                    }

                    (String::from(""), String::from(""))
                }
            })
        })
        .map(|x| x.join())
        .filter(|x| {
            if let Ok((v, _)) = x {
                return v != "";
            }
            false
        })
        .take(1)
        .next()
        .unwrap();

    handles.unwrap()
}
