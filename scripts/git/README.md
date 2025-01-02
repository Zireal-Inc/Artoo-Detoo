# GIT branch flow

<https://nvie.com/img/git-model@2x.png>

In this model, the primary branches are:

* **master** : The production-ready state of your code.
* **develop** : The integration branch for features.
* **feature/*** : Branches for developing new features.
* **release/*** : Branches for preparing new production releases.
* **hotfix/*** : Branches for quickly addressing production issues.

## Make Scripts Executable

After creating these scripts, make them executable with:

```sh
chmod +x script-name.sh
```

## Run Script

You can run each script by passing the required argument (e.g., feature name, release version):

```bash
./start-feature.sh my-feature-name
./finish-feature.sh my-feature-name

./start-release.sh v1.0.0 
./finish-release.sh v1.0.0

./start-hotfix.sh my-hotfix-name 
./finish-hotfix.sh my-hotfix-name 
```
