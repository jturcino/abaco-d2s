# abaco-d2s

A repo for [this Docker container](https://hub.docker.com/r/jturcino/abaco-d2s/) that runs [docker2singularity](https://github.com/TACC/docker2singularity) with [Abaco](https://github.com/TACC/abaco)

## Overview

The contents of this repo describe a Docker container that can be registered as an Abaco actor, which will transform a provided Docker container to a Singularity image and upload the image to a known storage system. The actor requires three inputs:
* **the Docker container** to transform to a Singularity image
* **the storage system** on which to save the Singularity image
* **the file path** at which to save the Singularity image

You can use cURL commands or the [abaco-cli](https://github.com/johnfonner/abaco-cli) to interface with abaco and use this repo. A tutorial with both cURL and the CLI are below. 

## Tutorial

This tutorial gives an overview of registering and running the `abaco-d2s` actor, providing both abaco-cli and cURL commands for each step. Please note that a SD2E token will be needed for both sets of commands. If you choose to use abaco-cli, please ensure you have JQ, getopts, and the [Agave CLI](https://bitbucket.org/agaveapi/cli) installed.

### 0. Setup
Get and save a valid SD2E access token.

**abaco-cli**
```
$ auth-tokens-create -S
Token for sd2e:jturcino successfully refreshed and cached for 14400 seconds
xxxxxxxxxxxxxxxxxx
```
**cURL**
```
$ TOKEN="xxxxxxxxxxxxxxxxxx"
```

### 1. Create the actor
Use `abaco create` or a POST command to create a privileged actor for the Docker container `jturcino/abaco-d2s:0.1.0`. Once done, make note of the actor ID (`WrPZake5ZWmaR`)

**abaco-cli**
```
$ ./abaco create -p -n d2s-tutorial jturcino/abaco-d2s:0.1.0
d2s-tutorial    WrPZake5ZWmaR
```
**cURL**
```
$ curl -X POST -sk -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" --data '{"image":"jturcino/abaco-d2s:0.1.0", "name":"d2s-tutorial", "privileged":true}' https://api.sd2e.org/actors/v2
{
  "message": "Actor created successfully.",
  "result": {
    "_links": {
      "executions": "https://api.sd2e.org/actors/v2/WrPZake5ZWmaR/executions",
      "owner": "https://api.sd2e.org/profiles/v2/jturcino",
      "self": "https://api.sd2e.org/actors/v2/WrPZake5ZWmaR"
    },
    "createTime": "2017-11-17 18:03:06.444248",
    "defaultEnvironment": {},
    "description": "",
    "id": "WrPZake5ZWmaR",
    "image": "jturcino/abaco-d2s:0.1.0",
    "lastUpdateTime": "2017-11-17 18:03:06.444248",
    "name": "d2s-tutorial",
    "owner": "jturcino",
    "privileged": true,
    "state": {},
    "stateless": false,
    "status": "SUBMITTED",
    "statusMessage": ""
  },
  "status": "success",
  "version": ":dev"
}
```
### 2. Check actor's status
Use `abaco list` or a GET command to check that the actor has `READY` status.

**abaco-cli**
```
$ ./abaco list
d2s-tutorial    WrPZake5ZWmaR    READY
```
**cURL**
```
$ curl -sk -H "Authorization: Bearer $TOKEN" https://api.sd2e.org/actors/v2/WrPZake5ZWmaR
{
  "message": "Actor retrieved successfully.",
  "result": {
    "_links": {
      "executions": "https://api.sd2e.org/actors/v2/WrPZake5ZWmaR/executions",
      "owner": "https://api.sd2e.org/profiles/v2/jturcino",
      "self": "https://api.sd2e.org/actors/v2/WrPZake5ZWmaR"
    },
    "createTime": "2017-11-15 20:54:43.132540",
    "defaultEnvironment": {},
    "description": "",
    "id": "WrPZake5ZWmaR",
    "image": "jturcino/docker-whale:latest",
    "lastUpdateTime": "2017-11-15 20:54:43.132540",
    "name": "d2s-tutorial",
    "owner": "jturcino",
    "privileged": true,
    "state": {},
    "stateless": false,
    "status": "READY",
    "statusMessage": ""
  },
  "status": "success",
  "version": ":dev"
}
```

### 3. Submit the job
Use `abaco submit` or a POST command to run the actor once its status is `READY`. The actor will require three inputs, which we pass in as a JSON string: the `container` to transform into a Singularity image, the `system` on which to store the image file, and the `outdir` (filepath) at which to save the image file. Once done, make note of the execution ID (`NNy8LrbNkzpWQ`).

**abaco-cli**
```
$ msg='{"container":"jturcino/docker-whale:latest", "system":"data-tacc-work-jturcino", "outdir":"/projects/docker/sd2e/"}'
$ ./abaco submit -m "$msg" WrPZake5ZWmaR
NNy8LrbNkzpWQ
{
  "container": "jturcino/docker-whale:latest",
  "outdir": "/projects/docker/sd2e/",
  "system": "data-tacc-work-jturcino"
}
```
**cURL**
```
$ msg='{"container":"jturcino/docker-whale:latest", "system":"data-tacc-work-jturcino", "outdir":"/projects/docker/sd2e/"}'
$ curl -sk -H "Authorization: Bearer $TOKEN"  -X POST -H "Content-Type: application/json" -d "$msg" https://api.sd2e.org/actors/v2/WrPZake5ZWmaR/messages?
{
  "message": "The request was successful",
  "result": {
    "_links": {
      "messages": "https://api.sd2e.org/actors/v2/WrPZake5ZWmaR/messages",
      "owner": "https://api.sd2e.org/profiles/v2/jturcino",
      "self": "https://api.sd2e.org/actors/v2/WrPZake5ZWmaR/executions/NNy8LrbNkzpWQ"
    },
    "executionId": "NNy8LrbNkzpWQ",
    "msg": {
      "container": "jturcino/docker-whale:latest",
      "outdir": "/projects/docker/sd2e/",
      "system": "data-tacc-work-jturcino"
    }
  },
  "status": "success",
  "version": ":dev"
}
```

### 4. Check job's status
Use `abaco executions` or a GET command to check that the job finished. Be sure to provide both the actor ID (`WrPZake5ZWmaR`) and the execution ID (`NNy8LrbNkzpWQ`).

**abaco-cli**
```
$ ./abaco executions -e NNy8LrbNkzpWQ WrPZake5ZWmaR
JK3WjNrR4WwqZ  COMPLETE
```
**cURL**
```
$ curl -sk -H "Authorization: Bearer $TOKEN" https://api.sd2e.org/actors/v2/WrPZake5ZWmaR/executions/NNy8LrbNkzpWQ
{
  "message": "Actor execution retrieved successfully.",
  "result": {
    "_links": {
      "logs": "https://api.sd2e.org/actors/v2/SD2E_WrPZake5ZWmaR/executions/NNy8LrbNkzpWQ/logs",
      "owner": "https://api.sd2e.org/profiles/v2/jturcino",
      "self": "https://api.sd2e.org/actors/v2/SD2E_WrPZake5ZWmaR/executions/NNy8LrbNkzpWQ"
    },
    "actorId": "WrPZake5ZWmaR",
    "apiServer": "https://api.sd2e.org",
    "cpu": 62168006,
    "executor": "jturcino",
    "exitCode": 0,
    "finalState": {
      "Dead": false,
      "Error": "",
      "ExitCode": 0,
      "FinishedAt": "2017-11-17T18:16:13.938886891Z",
      "OOMKilled": false,
      "Paused": false,
      "Pid": 0,
      "Restarting": false,
      "Running": false,
      "StartedAt": "2017-11-17T18:16:12.918472937Z",
      "Status": "exited"
    },
    "id": "NNy8LrbNkzpWQ",
    "io": 168,
    "messageReceivedTime": "2017-11-17 18:16:10.768702",
    "runtime": 1,
    "startTime": "2017-11-17 18:16:12.515289",
    "status": "COMPLETE",
    "workerId": "JK3WjNrR4WwqZ"
  },
  "status": "success",
  "version": ":dev"
}
```

### 5. Check job's logs
Use `abaco logs` or a GET command to check that the job ran properly by providing the actor ID and execution ID. If using the GET command, the log will likely be difficult to read. It is recommended to copy and paste the log output into a text editor and replace newline characters (`\n`) with actual newlines.

**abaco-cli**
```
$ ./abaco logs -e NNy8LrbNkzpWQ WrPZake5ZWmaR
Logs for execution NNy8LrbNkzpWQ:
RUNNING CONTAINER jturcino/docker-whale:latest
Size: 469 MB for the singularity container
(1/9) Creating an empty image...
Creating a sparse image with a maximum size of 469MiB...
Using given image size of 469
Formatting image (/sbin/mkfs.ext3)
Done. Image can be found at: /tmp/jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img
(2/9) Importing filesystem...
(3/9) Bootstrapping...
(4/9) Adding run script...
(5/9) Setting ENV variables...
(6/9) Adding mount points...
      /oasis /projects /scratch /local-scratch /work /home1 /corral-repl /beegfs /share/PI /extra
(7/9) Fixing permissions...
(8/9) Stopping and removing the container...
f73a5ba436eb
f73a5ba436eb
(9/9) Moving the image to the output folder...
    491,782,176 100%  153.36MB/s    0:00:03 (xfr#1, to-chk=0/1)

FINDING IMG FILE
/output/jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img

UPLOADING FILE
System ID: data-tacc-work-jturcino
Path: /projects/docker/sd2e/

PROCESS COMPLETE
```
**cURL**
```
$ curl -sk -H "Authorization: Bearer $TOKEN" https://api.sd2e.org/actors/v2/WrPZake5ZWmaR/executions/NNy8LrbNkzpWQ/logs
{
  "message": "Logs retrieved successfully.",
  "result": {
    "_links": {
      "execution": "https://api.sd2e.org/actors/v2/WrPZake5ZWmaR/executions/NNy8LrbNkzpWQ",
      "owner": "https://api.sd2e.org/profiles/v2/jturcino",
      "self": "https://api.sd2e.org/actors/v2/WrPZake5ZWmaR/executions/NNy8LrbNkzpWQ/logs"
    },
    "logs": "RUNNING CONTAINER jturcino/docker-whale:latest\nSize: 469 MB for the singularity container\n(1/9) Creating an empty image...\nCreating a sparse image with a maximum size of 469MiB...\nUsing given image size of 469\nFormatting image (/sbin/mkfs.ext3)\nDone. Image can be found at: /tmp/jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img\n(2/9) Importing filesystem...\n(3/9) Bootstrapping...\n(4/9) Adding run script...\n(5/9) Setting ENV variables...\n(6/9) Adding mount points...\n      /oasis /projects /scratch /local-scratch /work /home1 /corral-repl /beegfs /share/PI /extra\n(7/9) Fixing permissions...\n(8/9) Stopping and removing the container...\nf73a5ba436eb\nf73a5ba436eb\n(9/9) Moving the image to the output folder...\n\r         32,768   0%    0.00kB/s    0:00:00  \r    165,707,776  33%  158.00MB/s    0:00:02  \r    327,057,408  66%  156.02MB/s    0:00:01  \r    481,460,224  97%  153.14MB/s    0:00:00  \r    491,782,176 100%  153.36MB/s    0:00:03 (xfr#1, to-chk=0/1)\r    491,782,176 100%  153.36MB/s    0:00:03 (xfr#1, to-chk=0/1)\r    491,782,176 100%  153.36MB/s    0:00:03 (xfr#1, to-chk=0/1)\r    491,782,176 100%  153.36MB/s    0:00:03 (xfr#1, to-chk=0/1)\n\nFINDING IMG FILE\n/output/jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img\n\nUPLOADING FILE\nSystem ID: data-tacc-work-jturcino\nPath: /projects/docker/sd2e/\n\nPROCESS COMPLETE\n"
  },
  "status": "success",
  "version": ":dev"
}
```

### 6. View the image
Use the Agave CLI's `files-list` or a GET command to view the singularity image, should now be on the storage system as specified during job submission. 
**agave-cli**
```
$ files-list -S data-tacc-work-jturcino /projects/docker/sd2e/
.
jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img
```
**cURL**
```
$ curl -sk -H "Authorization: Bearer $TOKEN" https://api.sd2e.org/files/v2/listings/system/data-tacc-work-jturcino//projects/docker/sd2e/?pretty=true
{
  "status" : "success",
  "message" : null,
  "version" : "2.2.11-rd2c5cd6",
  "result" : [ {
    "name" : ".",
    "path" : "/projects/docker/sd2e",
    "lastModified" : "2017-11-17T12:27:11.000-06:00",
    "length" : 4096,
    "permissions" : "ALL",
    "format" : "folder",
    "mimeType" : "text/directory",
    "type" : "dir",
    "system" : "data-tacc-work-jturcino",
    "_links" : {
      "self" : {
        "href" : "https://api.sd2e.org/files/v2/media/system/data-tacc-work-jturcino//projects/docker/sd2e"
      },
      "system" : {
        "href" : "https://api.sd2e.org/systems/v2/data-tacc-work-jturcino"
      },
      "metadata" : {
        "href" : "https://api.sd2e.org/meta/v2/data?q=%7B%22associationIds%22%3A%223260320868200410649-242ac113-0001-002%22%7D"
      },
      "history" : {
        "href" : "https://api.sd2e.org/files/v2/history/system/data-tacc-work-jturcino//projects/docker/sd2e"
      }
    }
  }, {
    "name" : "jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img",
    "path" : "/projects/docker/sd2e/jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img",
    "lastModified" : "2017-11-17T12:27:19.000-06:00",
    "length" : 491782176,
    "permissions" : "READ_WRITE",
    "format" : "raw",
    "system" : "data-tacc-work-jturcino",
    "mimeType" : "application/octet-stream",
    "type" : "file",
    "_links" : {
      "self" : {
        "href" : "https://api.sd2e.org/files/v2/media/system/data-tacc-work-jturcino//projects/docker/sd2e/jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img"
      },
      "system" : {
        "href" : "https://api.sd2e.org/systems/v2/data-tacc-work-jturcino"
      }
    }
  } ]
}
```

### 7. Get the image
Use the Agave CLI's `files-get` or a GET command to download the Singularity image to you local machine.
**agave-cli**
```
$ files-get -S data-tacc-work-jturcino /projects/docker/sd2e/jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img
Downloading /projects/docker/sd2e/jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img ...
######################################################################## 100.0%
$ ls
jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img
```
**cURL**
```
curl -k -H "Authorization: Bearer $TOKEN" -O https://api.sd2e.org/files/v2/media/system/data-tacc-work-jturcino//projects/docker/sd2e/jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img
Downloading /projects/docker/sd2e/jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img ...
######################################################################## 100.0%
$ ls
jturcino_docker-whale_latest-2016-12-15-f73a5ba436eb.img
```