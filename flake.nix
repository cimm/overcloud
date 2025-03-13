{
  description = "Overcloud, an Overland backend";

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
        ]);
      in
      {
        apps.default = {
          type = "app";
          program = toString (pkgs.writeScript "overland" ''
            #!${pkgs.bash}/bin/bash
            export PYTHONPATH=${./.}:$PYTHONPATH
            ${pythonEnv}/bin/python ${./main.py} "$@"
          '');
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [
            pythonEnv
            pkgs.yapf
          ];
        };

        formatter = pkgs.nixpkgs-fmt;
      }
    );
}
