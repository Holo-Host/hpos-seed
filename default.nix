{ pkgs ? import ./nixpkgs.nix {} }:

with pkgs;
with python3Packages;

let
  qt5reactor = buildPythonPackage rec {
    pname = "qt5reactor";
    version = "0.5";

    src = fetchPypi {
      inherit pname version;
      sha256 = "1ghc3jypqy9iv43faddr9n520rn9hjw0wgzjwnb6b2cc30bizmsq";
    };

    propagatedBuildInputs = [ twisted ];
  };

  sphinxcontrib-asciinema = buildPythonPackage rec {
    pname = "sphinxcontrib.asciinema";
    version = "0.1.7";

    src = fetchPypi {
      inherit pname version;
      sha256 = "06mfs8hks44f7zf26g2p3wghksn2hkcim2rdlibmcnj0kpzrqwr6";
    };

    propagatedBuildInputs = [ sphinx ];
  };

  sphinxcontrib-mermaid = buildPythonPackage rec {
    pname = "sphinxcontrib_mermaid";
    version = "0.3.1";
    format = "wheel";

    src = fetchPypi {
      inherit pname version format;
      sha256 = "1rwmfp8bgd5qpjfizydq2zznrjl58ayxq45jjd0p44iwqqlkbqyj";
    };
  };

  hpos-seed = buildPythonPackage {
    name = "hpos-seed";
    src = lib.cleanSource ./.;

    nativeBuildInputs = [ qt5.wrapQtAppsHook ];

    propagatedBuildInputs = [
      magic-wormhole
      pyqt5
      qt5reactor
      sphinx
      sphinxcontrib-asciinema
      sphinxcontrib-mermaid
    ];

    setupPyBuildFlags = [ "build_sphinx" ];

    postInstall = ''
      mkdir -p $out/nix-support
      echo "doc manual $out/share/doc/hpos-seed" > $out/nix-support/hydra-build-products

      mkdir -p $out/share/doc
      cp -r build/sphinx/html $out/share/doc/hpos-seed
    '';

    meta.platforms = lib.platforms.all;
  };

  hpos-seed-roundtrip = nixosTest {
    name = "hpos-seed-roundtrip";

    nodes = {
      relay = {
        imports = [ "${holo-nixpkgs.path}/profiles" ];
        networking.firewall.allowedTCPPorts = [ 4000 ];
        services.magic-wormhole-mailbox-server.enable = true;
      };

      receiver = {
        environment.systemPackages = [ hpos-seed ];
        services.mingetty.autologinUser = "root";
      };

      sender = {
        environment.systemPackages = [ hpos-seed ];
      };
    };

    testScript = ''
      startAll;

      $relay->waitForUnit("magic-wormhole-mailbox-server.service");
      $relay->waitForOpenPort(4000);

      $receiver->waitUntilTTYMatches(1, "\$");
      $receiver->sendChars("HPOS_SEED_RELAY_URL=ws://relay:4000/v1 hpos-seed-receive > hpos-config-a.json\n");
      $receiver->waitUntilTTYMatches(1, "Wormhole code:");

      (my $wormhole_code) = $receiver->getTTYText(1) =~ m/(\d+-\w+-\w+)/;

      $sender->copyFileFromHost("${./docs/hpos-config.json}", "hpos-config.json");
      $sender->succeed("HPOS_SEED_RELAY_URL=ws://relay:4000/v1 hpos-seed-send $wormhole_code hpos-config.json");

      $receiver->copyFileFromHost("${./docs/hpos-config.json}", "~/hpos-config-b.json");
      $receiver->succeed("cmp ~/hpos-config-a.json ~/hpos-config-b.json");
    '';
  };
in

{ inherit hpos-seed hpos-seed-roundtrip; }
