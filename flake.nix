{
  description = "OverCloud Server Development Environment";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          geopandas
          shapely
        ]);

      in
      with pkgs; {
        devShells.default = mkShell {
          buildInputs = [
            pythonEnv
            yapf
          ];
        };

        formatter = pkgs.nixpkgs-fmt;
      }
    );
}
