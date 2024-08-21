# dora_rviz
```sh
pip install dora-rs==0.3.5 --break-system-packages
git checkout tags/v0.3.5
cargo build -p dora-cli --release
cargo run --example cxx-dataflow  # compile C++ node
cargo build -p dora-node-api-c --release  # compile dora-node-api-c 
cargo run --example cxx-ros2-dataflow --features ros2-examples
```