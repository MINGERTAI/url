name: xyz
on:
  workflow_dispatch:
    
  schedule:
    - cron: '5 */4 * * *'

jobs:
  run_python_script:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5 
      with:
        python-version: 3.x

    - name: Install dependencies
      run: |
        pip install requests

    - name: Run Python script
      run: python ./fan/xyz.py

    - id: check
      name: Check for changes
      run: |
        git config --global user.name "GitHub Actions"
        git config --global user.email "actions@github.com"
        git add .
        git commit -m "update"
        #commit_msg="更新并删除删除无效节点"
        #git commit -a --allow-empty -m "$commit_msg"

    - name: Push changes
      if: steps.check.conclusion == 'success'
      uses:  ad-m/github-push-action@master
      with:
         github_token: ${{ secrets.GITHUB_TOKEN }}
         # github_token: ${{ secrets.TOKEN }}
         branch: main
         #force: true
      #env:
        #GITHUB_ACTOR: ne7359

    - name: Delete Workflow Runs
      uses: Mattraks/delete-workflow-runs@main
      continue-on-error: true
      with:
        token: ${{ github.token }}
        repository: ${{github.repository}}
        retain_days: 0
        keep_minimum_runs: 1
