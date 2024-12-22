// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IPFXStorage {

    struct HashRecord {
        string hashID;          
        address userAddress;    
        uint256 timeStamp;      
    }

    mapping(bytes32 => HashRecord) public hashRecords;

    uint256 public  idCounter;

    event HashStored(bytes32 uniqueID, string hashID, address indexed userAddress, uint256 timeStamp);

    // Function to store hash and generate a unique ID
    function storeHash(string memory hashID) public returns (bytes32){
        require(bytes(hashID).length > 0, "Hash ID cannot be empty");
        idCounter++;
        bytes32 uniqueId = keccak256(abi.encodePacked(idCounter));

        hashRecords[uniqueId] = HashRecord(hashID, msg.sender, block.timestamp);

        emit HashStored(uniqueId, hashID, msg.sender, block.timestamp);

        return uniqueId;
    }

    // Function to retrieve hash details using the unique ID
    function getHashDetails(bytes32 uniqueID) public view returns (string memory, address, uint256) {
        require(bytes(hashRecords[uniqueID].hashID).length > 0, "Hash does not exist");

        HashRecord memory record = hashRecords[uniqueID];
        return (record.hashID, record.userAddress, record.timeStamp);
    }
}
