# Foundry - Smart Contract Development and Lifecycle Management Tool

Sample Repo found [here](https://github.com/Taraxa-project/foundry-example/tree/main).

Welcome to Foundry, a comprehensive tool designed to streamline the development and management of smart contracts on the Taraxa platform. This README provides a detailed guide for new developers looking to utilize Foundry for their smart contract needs.

## Table of Contents

- [Foundry - Smart Contract Development and Lifecycle Management Tool](#foundry---smart-contract-development-and-lifecycle-management-tool)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Scripts](#scripts)
  - [Deploying a contract](#deploying-a-contract)
  - [Importance of the --legacy flag while working with Taraxa networks](#importance-of-the---legacy-flag-while-working-with-taraxa-networks)
  - [Writing your first Foundry script](#writing-your-first-foundry-script)

## Introduction

Foundry is a powerful tool that simplifies the process of developing, testing, and deploying smart contracts on the Taraxa platform. It provides a robust and flexible framework that allows developers to focus on the logic of their contracts, rather than the intricacies of the platform. You can read their documentation [here](https://book.getfoundry.sh/).

## Installation

Before you can start using Foundry, you need to install it on your system. Follow the instructions described in their [installation guide](https://book.getfoundry.sh/installation).

If you have any doubts about the setup of a Foundry project, please visit the [official project layout page](https://book.getfoundry.sh/projects/project-layout).

## Usage

To start using Foundry, follow the steps below:

1. To create a new Foundry project: `$ forge init new_foundry_project`
2. Compile the contracts: `$ forge build`
3. Test the contracts: `forge test`

For more detailed instructions and usage examples, refer to the [official documentation](https://taraxa.io/docs/foundry).

For the sake of simplicity, this repo is wrapped with a package.json file that allows you to run the commands above with `yarn <command>`. For example, to compile the contracts, you can run `yarn build`.

## Scripts

In order to deploy or interact with smart contracts via Foundry, you can use the scripts provided in the `scripts` directory. These scripts are natively written in Solidity and can be used to deploy, interact, and test smart contracts. For more information on how to use these scripts, refer to the [official documentation](https://book.getfoundry.sh/tutorials/solidity-scripting).

## Deploying a contract

To deploy a contract, you'll need the private key of a wallet that has enough funds to deploy the contract. You can use the sample deployment command provided in the package.json file to deploy the contract. For example, to deploy the `DemoTara` contract, you can run `yarn deploy`.

## Importance of the --legacy flag while working with Taraxa networks

Taraxa, at the moment of recording, does not support [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559), therefore it still requires the old RPC transaction fee format. This means that you need to use the `--legacy` flag when sending transactions to the network.

## Writing your first Foundry script
