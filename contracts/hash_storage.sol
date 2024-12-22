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

    function storeHash(string memory hashID, address userAddress, uint256 timeStamp) public {
        require(bytes(hashID).length > 0, "Hash ID cannot be empty");

        require(hashRecords[hashID].timeStamp == 0, "Hash already exists");

        // Create an Evidence struct
        HashRecord memory newEvidence = HashRecord({
            hashID: hashID,
            userAddress: msg.sender,
            timestamp: block.timestamp
        });

        // Add the hash record to the blockchain
        hashRecords[hashID] = HashRecord(hashID, userAddress, timeStamp);

        // Emit an event
        emit HashStored(hashID, msg.sender, block.timestamp);
    }

    // Function to retrieve hash details
    function getHashDetails(string memory hashID) public view returns (string memory, address, uint256) {
        require(hashRecords[hashID].timeStamp != 0, "Hash does not exist");

        HashRecord memory record = hashRecords[hashID];
        return (record.hashID, record.userAddress, record.timeStamp);
    }
}
