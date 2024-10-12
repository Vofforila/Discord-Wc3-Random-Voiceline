{pkgs}: {
  deps = [
    pkgs.libopus
    pkgs.libsodium
    pkgs.ffmpeg
    pkgs.python39Full
    pkgs.python39Packages.pip
  ];
}
