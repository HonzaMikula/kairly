workflow "On Milestone" {
  on = "milestone"
  resolves = ["Create Release Notes"]
}

action "Create Release Notes" {
  uses = "Decathlon/release-notes-generator-action@master"
  secrets = ["GITHUB_TOKEN"]
  env = {
    USE_MILESTONE_TITLE = "true"
  }
}
