{
  description = "Voice Mode - Natural voice conversations for AI assistants";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        
        pythonEnv = pkgs.python312.withPackages (ps: with ps; [
          pip
          setuptools
          wheel
          virtualenv
        ]);
        
        # Wrapper script that uses uvx with proper LD_LIBRARY_PATH
        voice-mode = pkgs.writeShellScriptBin "voice-mode" ''
          export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
            pkgs.portaudio
            pkgs.libpulseaudio
            pkgs.alsa-lib
            pkgs.stdenv.cc.cc.lib
          ]}:$LD_LIBRARY_PATH"
          
          exec ${pkgs.uv}/bin/uvx voice-mode "$@"
        '';
      in
      {
        packages.default = voice-mode;
        
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            # Python
            pythonEnv
            uv
            
            # Audio libraries
            portaudio
            libpulseaudio
            alsa-lib
            ffmpeg
            
            # Development headers and tools
            pkg-config
            
            # Audio tools
            pulseaudio
            alsa-utils
            
            # Additional tools
            git
          ];
          
          shellHook = ''
            echo "Voice Mode NixOS development environment"
            echo "Python ${pkgs.python312.version} with uv and audio dependencies"
            
            # Set up library paths
            export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath [
              pkgs.portaudio
              pkgs.libpulseaudio
              pkgs.alsa-lib
              pkgs.stdenv.cc.cc.lib
            ]}:$LD_LIBRARY_PATH"
            
            # Set up pkg-config
            export PKG_CONFIG_PATH="${pkgs.portaudio}/lib/pkgconfig:${pkgs.libpulseaudio}/lib/pkgconfig:$PKG_CONFIG_PATH"
            
            # Create venv if it doesn't exist
            if [ ! -d .venv ]; then
              echo "Creating virtual environment..."
              uv venv
            fi
            
            echo ""
            echo "To activate the virtual environment, run: source .venv/bin/activate"
            echo "Then install voice-mode with: uv pip install -e ."
            echo "Or run directly with: uvx voice-mode"
          '';
        };
      });
}