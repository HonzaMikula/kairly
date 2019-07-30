workflow "New workflow" {
  resolves = ["release-notes-generator-action"]
  on = "milestone"
}

action "release-notes-generator-action" {
  uses = "Decathlon/release-notes-generator-action@v1.0.1"
  secrets = ["GITHUB_TOKEN"]
  env = {
    USE_MILESTONE_TITLE = "true"
  }
}
