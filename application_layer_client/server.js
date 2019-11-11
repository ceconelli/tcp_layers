const fs = require('fs')
const lockfile = require('proper-lockfile');

class User {


    constructor(address) {

        this.address = address;
        this.inbox = [];

        this.emailServer = new EmailServer();
        this.emailServer.userList.push(this);

    }


    writeEmail(to,data) {
        
        // fs.writeFile("./messages/sent/file.txt", data, (err) => {
        //     if (err) console.log(err);-
        //     console.log("Successfully Written to File.");
        // });

    }

}

class EmailServer {

    constructor() {
        this.userList = [];
    }
}

module.exports = {User,EmailServer}