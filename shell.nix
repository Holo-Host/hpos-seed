{ pkgs ? import ./nixpkgs.nix {} }:

with pkgs;

mkShell {
  inputsFrom = lib.attrValues (import ./. { inherit pkgs; });

  buildInputs = [
    asciinema
    nixpkgs-fmt
    python3Packages.autopep8
    python3Packages.flake8
  ];

  shellHook = ''
    # https://nixos.org/nixpkgs/manual/#python-setup.py-bdist_wheel-cannot-create-.whl
    unset SOURCE_DATE_EPOCH
  '';

  QML2_IMPORT_PATH = lib.concatStringsSep ":" [
    "${qt5.qtdeclarative.bin}/${qt5.qtbase.qtQmlPrefix}"
    "${qt5.qtquickcontrols}/${qt5.qtbase.qtQmlPrefix}"
  ];

  QT_PLUGIN_PATH = "${qt5.qtbase.bin}/${qt5.qtbase.qtPluginPrefix}";
}
