{
  nixpkgs ? (builtins.fetchGit {
    name = "nixos-unstable-2020-11-25";
    url = "https://github.com/nixos/nixpkgs-channels/";
    # `git ls-remote https://github.com/nixos/nixpkgs-channels nixos-unstable`
    ref = "refs/heads/nixos-unstable";
    rev = "84d74ae9c9cbed73274b8e4e00be14688ffc93fe";
  })
}:

let
  pkgs = import nixpkgs {};
in
pkgs.mkShell rec {
  name = "splitbills_server";

  venvDir = "./.venv";

  buildInputs = with pkgs; [
    python39Packages.python
    python39Packages.venvShellHook
  ];

  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    pip install -r requirements_lock.txt
  '';

  postShellHook = ''
    unset SOURCE_DATE_EPOCH
  '';
}
