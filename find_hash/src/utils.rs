use rand::{thread_rng, Rng};
use rayon::prelude::*;
use sha2::{Digest, Sha256};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;
use std::thread;
use tokio::time::Instant;

pub fn generate_nonce(buffer: &mut [u8]) {
    let charset = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    let mut rng = thread_rng();
    for byte in buffer.iter_mut() {
        *byte = charset[rng.gen_range(0..charset.len())];
    }
}

pub fn generate_hash(data: &[u8]) -> String {
    let hash = Sha256::digest(data);
    format!("{:x}", hash)
}

pub async fn find_hash(mission_hash: &str, require: &str, cores: usize) -> (String, String) {
    let mission_hash_bytes = mission_hash.as_bytes();
    let mut global_found = Arc::new(AtomicBool::new(false));
    let required_len = require.len();

    let result = (0..cores)
        .into_par_iter()
        .map(|_| {
            let global_found = Arc::clone(&global_found);
            let mut nonce = vec![0u8; 48];
            let mut buffer = vec![0u8; mission_hash.len() + 48];

            buffer[..mission_hash_bytes.len()].copy_from_slice(mission_hash_bytes);

            while !global_found.load(Ordering::Relaxed) {
                generate_nonce(&mut nonce);
                buffer[mission_hash_bytes.len()..].copy_from_slice(&nonce);
                let hash = generate_hash(&buffer);

                if hash.starts_with(require) {
                    global_found.store(true, Ordering::Relaxed);
                    return (String::from_utf8(nonce).unwrap(), hash);
                }
            }
            (String::new(), String::new())
        })
        .find_any(|(nonce, _)| !nonce.is_empty())
        .unwrap_or((String::new(), String::new()));

    result
}
