// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import "lib/forge-std/src/Script.sol";
import "src/DemoTara.sol";

contract DeployDemoTara is Script {
    function run() public {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        DemoTara demoTara = new DemoTara();

        vm.stopBroadcast();
    }
}
