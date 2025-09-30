# Frontend

## Useful links

* [axs-web-3d-libraries repository](https://github.com/straumann/axs-web-3d-libraries)
* [axs-patients repository](https://dev.azure.com/stgcs-cx/OnePortal/_git/axs-patients)
* [axs-solution repository](https://dev.azure.com/stgcs-cx/OnePortal/_git/axs-solution)
* [conventional commits specs](https://www.conventionalcommits.org/en/v1.0.0/)
* [storybook - dev environment](https://wwwstgoneportaldev.z6.web.core.windows.net/viewer-components/)

## Repo

The frontend repository of Webcad is [axs-web-3d-libraries](https://github.com/straumann/axs-web-3d-libraries), currently available on Github. In the packages folder, you will find a module for each Webcad feature (model builder, abutment editor...). A `README` is available to help you setup the project.

## Development

Since this repo is on GitHub and not Gerrit, to push your code, you need to create a new branch and push it, then create a pull request on GitHub.

### Pull requests guidelines

When creating a new Pull Request, make sure the name of your PR matches the [conventional commits specs](https://www.conventionalcommits.org/en/v1.0.0/). A check is run and will fail if it's not the case.

Your commits should also be **Verified**. To do that, you will need to [sign your commits with you ssh key](https://docs.github.com/en/authentication/managing-commit-signature-verification/telling-git-about-your-signing-key#telling-git-about-your-ssh-key) and [upload your ssh key as a signing key to your GitHub account](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account) (This link is about GPG key, but it can also be done with a SSH key).

You can push as many commits as you want on your branch, you can also push new commits even after the Pull Request has been opened. When merging the PR, GitHub will let you squash all the commits into one before merging onto the main branch.

## Deployment

When you PR is merged, it will be automatically be deployed on the [storybook](https://wwwstgoneportaldev.z6.web.core.windows.net/viewer-components/) on the dev environment.

If you need to deploy your changes on AXS too, this deployment is managed by the [axs-patients](https://dev.azure.com/stgcs-cx/OnePortal/_git/axs-patients) repository. Clone this repo.

This repo contains an `axs-patients-frontend` module. The `package.json` of this module contains the version of model builder and all other components from [axs-web-3d-libraries](https://github.com/straumann/axs-web-3d-libraries) that are currently deployed on AXS.

To deploy a new version, first create a new work item in your Azure Board if there is no Azure work item for your changes yet (Example: [Saiyan Azure board](https://dev.azure.com/stgcs-cx/OnePortal/_boards/board/t/Scrum%20Team%20-%20Saiyan/User%20stories)).

Go to the `package.json` of `axs-patients-frontend` and update the versions of the dependencies that need to be updated. Run the `yarn` command to also regenerate the `yarn.lock` file. You will need to include the new `yarn.lock` in your commit.

Create a new branch, make sure you respect the conventions written in the `README` of the `axs-patients-frontend` module for the branch name and commit message. You can then push your commit and create a Pull Request on [axs-patients](https://dev.azure.com/stgcs-cx/OnePortal/_git/axs-patients).

You will need to notify team ST8 of that Pull Request as they are marked as required reviewers.

Once the PR will be merged, your changes will be deployed on AXS `dev02` environment.

## Publish a HotFix

You can publish a hotfix if a change needs to be deployed on PPR or prod rapidly.

First, you need all steps in the [Deployment](#deployment) section to be done.

The deployment on PPR and prod are done in the [axs-solution](https://dev.azure.com/stgcs-cx/OnePortal/_git/axs-solution) repository, clone this repo.
You then need to go check the [axs-patients-frontend Azure pipeline](https://dev.azure.com/stgcs-cx/OnePortal/_build?definitionId=190) and find the version number of the commit you wish to publish.

In [axs-solution](https://dev.azure.com/stgcs-cx/OnePortal/_git/axs-solution), create a new branch called `hotfix/<your version number>-<change description>`
Open the `solbom-versions.json` file, and change the version of `axs-patients-frontend` to the new version number.

Push your branch and create a Pull Request on Azure. You will then need to make a hotfix request, this is done through a private channel on Teams, you can mention on the `Web Apps Development` channel that you would like to make a hotfix request. Once the request is done, all the required reviewers need to approve the Pull Request so it can then be deployed to PPR. Once the changes are deployed on PPR, test them to make sure everything works correctly, if it's all good, mention it again on Teams and the changes will be deployed on prod.