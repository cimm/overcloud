{
  description = "OverCloud, an Overland backend";

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
        packages.default = pkgs.stdenv.mkDerivation {
          name = "run-overcloud";
          src = ./.;
          buildInputs = [ pythonEnv ];
          buildPhase = "python main.py";
          installPhase = "mkdir -p $out/bin && cp $buildScript $out/bin/run-overcloud";
          buildScript = pkgs.writeShellScript "run-overcloud-script" ''
            #!${pythonEnv}/bin/python
            python main.py
          '';
        };

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
#{
#  description = "OverCloud, an Overland backend";
#
#  inputs = {
#    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.11";
#    flake-utils.url = "github:numtide/flake-utils";
#  };
#
#  outputs = { self, nixpkgs, flake-utils }:
#    flake-utils.lib.eachDefaultSystem (system:
#      let
#        pkgs = nixpkgs.legacyPackages.${system};
#
#        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
#          geopandas
#          shapely
#        ]);
#
#      in
#      with pkgs; {
#        devShells.default = mkShell {
#          buildInputs = [
#            pythonEnv
#            yapf
#          ];
#        };
#
#        formatter = pkgs.nixpkgs-fmt;
#      }
#    );
#}
