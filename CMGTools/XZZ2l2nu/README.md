X->ZZ->2l2nu Analysis Package
===============================

  Analysis package heavy resonnance search using X->ZZ->2l2nu final states.

Note: this is for 74x analysis. For 76x analysis the package moved to :
https://github.com/MMHY/cmgtools-lite/tree/xzz2l2nu_76x/XZZ2l2nu 

Instructions for package development.
---------------------------------

1. Setup Environment

  ```
  release=CMSSW_7_4_12_patch4
  tag=""
  export SCRAM_ARCH=slc6_amd64_gcc491
  alias cmsenv='eval `scramv1 runtime -sh`'
  alias cmsrel='scramv1 project CMSSW'

  scram project -n ${release}${tag} $release
  cd ${release}${tag}/src
  cmsenv
  ```

2. Create empty repository (with the cmssw trick to keep the repository small)

  ```
  git cms-init
  ```

3. Add MMHY repository which contains the CMGTools/XZZ2l2nu package, and fetch it

  ```
  git remote add mmhy https://github.com/MMHY/cmg-cmssw.git
  git fetch mmhy
  ```

4. Configure the sparse checkout (to only checkout needed packages)

  ```
  curl -O https://raw.githubusercontent.com/MMHY/cmg-cmssw/xzz2l2nu_v1/CMGTools/XZZ2l2nu/tools/sparse-checkout
  mv sparse-checkout .git/info/sparse-checkout
  ```

5. Checkout the CMGTools/XZZ2l2nu package, currently the main branch is xzz2l2nu_v1

  ```
  git checkout -b xzz2l2nu_v1 mmhy/xzz2l2nu_v1
  ```

6. Add your mirror (see https://twiki.cern.ch/twiki/bin/viewauth/CMS/CMGToolsGitMigration#Prerequisites )

  ```
  git remote add origin https://github.com/<your own github name>/cmg-cmssw.git
  ```
  Don't for get to replace "<your own github name>" with your own github user name.

 
7. Push the package CMGTools/XZZ2l2nu in the branch xzz2l2nu_v1 into your own github repository

  ```
  git push origin xzz2l2nu_v1
  ```

8. Make a copy of branch xzz2l2nu_v1 for your own developement, you can choose a branch name as you want, such as xzz2l2nu_v1_mydev

  ```
  git checkout -b xzz2l2nu_v1_mydev
  ```

9. Please frequently commit your changes and push your development branch to your own repository

  ```
  git commit -m 'describe your change here.' -a
  git push origin xzz2l2nu_v1_mydev
  ```


10. Once your developement is done, you can update the central branch xzz2l2nu_v1 with a Pull Request. Steps below:

  * Update the branch xzz2l2nu_v1 in your local repository with others developements on mmhy
    ```
    git checkout xzz2l2nu_v1
    git fetch mmhy 
    ```

  * Rebased your development branch to the head of xzz2l2nu_v1, and update it in your own repository
    ```
    git checkout xzz2l2nu_v1_mydev
    git merge xzz2l2nu_v1
    git push origin xzz2l2nu_v1_mydev
    ```

11. Make a PR from branch xzz2l2nu_v1_mydev in your own respository to branch xzz2l2nu_v1 in MMHY respository to let others cross-check your changes. Once looks good, merge it.

  The PR can be created on the webpage of your own repository:

      https://github.com/<your own github name>/cmg-cmssw/tree/xzz2l2nu_v1_mydev

  E.g. A PR from hengne's xzz2l2nu_v1_mydev branch to MMHY's xzz2l2nu_v1 will look like this in the following link:

      https://github.com/MMHY/cmg-cmssw/compare/xzz2l2nu_v1...hengne:xzz2l2nu_v1_mydev  

  **Let's make it a rule here: Please always let other collabrators to view and sign your PR before merging it, even if you have the permission to do it all by yourself.**
  

