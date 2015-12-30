X->ZZ->2l2nu Analysis Package
===============================

  Analysis package heavy resonnance search using X->ZZ->2l2nu final states.
 

Instructions to run the package.
---------------------------------

### Setup Environment

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

### Create empty repository (with the cmssw trick to keep the repository small)

```
git cms-init
```

### Add MMHY repository which contains the CMGTools/XZZ2l2nu package, and fetch it

```
git remote add mmhy https://github.com/MMHY/cmg-cmssw.git
git fetch mmhy
```

### Configure the sparse checkout (to only checkout needed packages)

```
curl -O https://raw.githubusercontent.com/MMHY/cmg-cmssw/xzz2l2nu_v1/CMGTools/XZZ2l2nu/tools/sparse-checkout
mv sparse-checkout .git/info/sparse-checkout
```

### Checkout the CMGTools/XZZ2l2nu package, currently the main branch is xzz2l2nu_v1

```
git checkout -b xzz2l2nu_v1 mmhy/xzz2l2nu_v1
```

### Add your mirror (see https://twiki.cern.ch/twiki/bin/viewauth/CMS/CMGToolsGitMigration#Prerequisites )

```
git remote add origin https://github.com/<your own github name>/cmg-cmssw.git
```
  Don't for get to replace ```<your own github name>``` with your own github user name.


### Push the package CMGTools/XZZ2l2nu in the branch xzz2l2nu_v1 into your own github repository

```
git push origin xzz2l2nu_v1
```

### Make a copy of branch xzz2l2nu_v1 for your own developement, you can choose a branch name as you want, such as xzz2l2nu_v1_mydev

```
git checkout -b xzz2l2nu_v1_mydev
```

### You can frequently push your development branch to your own repository

```
git push origin xzz2l2nu_v1_mydev
```


### Once your developement is done, you can update the central branch xzz2l2nu_v1 with a Pull Request. Steps below:

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

* Make a PR from branch xzz2l2nu_v1_mydev in your own respository to branch xzz2l2nu_v1 in MMHY respository to let others cross-check your changes. Once looks good, merge it.
  The PR can be created on the webpage of your own repository:

      https://github.com/<your own github name>/cmg-cmssw/tree/xzz2l2nu_v1_mydev

  
# add the central CMG repository, and fetch it
# limit the fetch to the 7_4_12-related branches, to avoid loading all the past history of CMGTools
git remote add cmg-central https://github.com/CERN-PH-CMG/cmg-cmssw.git  -f -t CMGTools-from-CMSSW_7_4_12 -t heppy_74X
git fetch cmg-central


# checkout the CMGTools branch of the release, and push it to your CMG repository
git checkout -b CMGTools-from-CMSSW_7_4_12 cmg-central/CMGTools-from-CMSSW_7_4_12
git push -u origin CMGTools-from-CMSSW_7_4_12

# create also the heppy branch
#git branch heppy_74X cmg-central/heppy_74X

# get this package
git remote add hengne https://github.com/hengne/cmg-cmssw.git
git fetch hengne



# combine
#git clone -b 74x-root6 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
#git clone https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement.git ZZMatrixElement
#git clone https://github.com/gpetruc/HiggsAnalysis-ZZMatrixElement.git ZZMatrixElement

#compile
scram b -j 8

