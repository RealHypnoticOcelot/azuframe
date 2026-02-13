{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { nixpkgs, ... }:
  let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};
  in
  {
    devShells.${system}.default = pkgs.mkShell {
      packages = with pkgs; [
        (python3.withPackages (python-pkgs: with python-pkgs; [
          discordpy
          ffmpeg-python
          wand
        ]))
        ffmpeg
        imagemagick
      ];
    };
  };
}
# Run `nix develop` to enter a shell containing python, and run `exit` to leave the shell