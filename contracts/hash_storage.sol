// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract IPFXStorage {

    struct HashRecord {
        string hashID;           
        address userAddress;     
        uint256 timeStamp;       
    }
    
    mapping(string => HashRecord) public hashRecords;

    event HashStored(string hashID, address indexed userAddress, uint256 timeStamp);

    function storeHash(string memory _hashID) public {
        require(bytes(_hashID).length > 0, "Hash ID cannot be empty");

        // Ensure that the hashID does not already exist
        require(hashRecords[_hashID].timeStamp == 0, "Hash already exists");

        // Add the hash record to the blockchain
        hashRecords[_hashID] = HashRecord({
            hashID: _hashID,
            userAddress: msg.sender, 
            timeStamp: block.timestamp 
        });

        // Emit an event
        emit HashStored(_hashID, msg.sender, block.timestamp);
    }

    // Function to retrieve hash details
    function getHashDetails(string memory _hashID) public view returns (string memory, address, uint256) {
        require(hashRecords[_hashID].timeStamp != 0, "Hash does not exist");

        HashRecord memory record = hashRecords[_hashID];
        return (record.hashID, record.userAddress, record.timeStamp);
    }
}
