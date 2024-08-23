use core::hash;

use clap::Parser;
mod utils;

#[derive(Parser)]
struct Args {
    mission_hash: String,

    require: String,

    cores: u8,
}

#[tokio::main]
async fn main() {
    let args = Args::parse();

    let (nonce, hash) =
        utils::find_hash(&args.mission_hash, &args.require, (args.cores as u8).into()).await;

    println!("{}", nonce);
    println!("{}", hash);
}
