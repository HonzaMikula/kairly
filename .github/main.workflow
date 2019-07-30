workflow "On Milestone" {
  on = "milestone"
  resolves = ["Upload Release Notes on Wiki"]
}

action "Create Release Notes" {
  uses = "Decathlon/release-notes-generator-action@master"
  secrets = ["GITHUB_TOKEN"]
  env = {
    USE_MILESTONE_TITLE = "true"
    OUTPUT_FOLDER = "temp_release_notes"
  }
}

action "Upload Release Notes on Wiki" {
  uses = "Decathlon/wiki-page-creator-action@master"
  needs = ["Create Release Notes"]
  secrets = [
    "GH_PAT",
    "GITHUB_TOKEN",
  ]
  env = {
    ACTION_MAIL = "jan.mikula@hotmail.com"
    REPO_NAME = "kairly"
    SKIP_MD = "README.md"
    MD_FOLDER = "temp_release_notes"
    OWNER = "honzamikula"
    ACTION_NAME = "honzamikula"
  }
}
