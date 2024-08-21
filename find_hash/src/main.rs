use clap::Parser;
mod utils;

// Define the structure of the command-line arguments
#[derive(Parser)]
struct Args {
    /// The mission hash
    mission_hash: String,

    /// The required prefix
    require: String,

    /// Number of CPU cores to use
    cores: u8,
}

#[tokio::main]
async fn main() {
    // Parse the command-line arguments
    let args = Args::parse();

    let (nonce, _) = utils::find_hash(&args.mission_hash, &args.require, args.cores).await;

    println!("{}", nonce);
    // println!("{}", hash);
}
