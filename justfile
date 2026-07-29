set positional-arguments

default:
    @just --list

# Run a focused Cargo test by substring pattern.
test-one pattern:
    @test -n "{{pattern}}" || (echo "usage: just test-one <pattern>" >&2; exit 64)
    cargo test --workspace "{{pattern}}"
