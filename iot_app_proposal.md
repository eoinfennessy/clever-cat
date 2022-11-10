# [😸 Clever Cat](https://github.com/eoinfennessy/clever-cat) - AI Animal Feeder

#### Student Name: *Eoin Fennessy*

#### Student ID: *20100018*

Problem: Existing automated cat feeders may end up feeding more than just your feline friend! 🐀🐭🐁 They may also be unable to keep track of when your animal has eaten or let you know that your animal is safe and accounted for while you are away.

Solution: **Clever Cat** is a smart animal feeder equipped with a camera and electronic feed dispenser that utilises AI technologies to ensure that your cat (and only your cat) gets fed when it is detected by the camera.

The accompanying mobile/web app can notify you when your cat is fed, display feeding/sighting analytics, and even retrieve live pictures of your pet while you are away. The app also allows the user to control how much food should be dispensed and how often, as well as giving an estimate of how much food is left in the hopper.

---

## Tools, Technologies and Equipment

##### Device

Raspberry Pi connected to camera module (for sensing cat) and servo motor (for actuating feeder). The pi will run a Python app using libraries such as OpenCV and Pytorch to sense when a (specific?) cat has been detected. The app will set up both publish and subscribe connections to an MQTT broker (Maybe using Paho) for sending feeding/sighting data and cat pics, and receiving config setting changes from the user.

##### MQTT Broker

Maybe Mosquitto running on a VM somewhere?

##### Message Handler

A Python or Node service for receiving subscribed data from the broker and populating the DB and file server with it, as well as perhaps handling the sending of push notifications to the frontend app, or other types of user-bound messages (WhatsApp, email with SMTP, etc.). This service will also listen for changes to the device config in the DB and publish the changes to the message broker.

##### Backend

Would love to try using [Pocketbase](https://pocketbase.io/) (a self-hosted Firebase alternative) to keep everything self-hostable... Rubric asks for "excellent use of cloud/IoT specific platforms" – Could this requirement by satisfied if running Pocketbase on a VM somewhere like Linode or Digital Ocean? This service will offer simple HTTP APIs for CRUD operations on DB, and *might* be extended (using Go) with some functionality for sending messages (emails?) to user on certain events, or maybe directly publish device config to MQTT broker.

##### Frontend

Either a simple dynamic JS web app (maybe Svelte/Next.JS) or a Flutter app that uses push notifications to update user.

##### Other Technologies

Docker for containerising all services. docker-compose file for quick build and deployment of dev environment. VS Code with Remote SSH plugin for development.

##### ML Ops

Very much a stretch goal: Use the hundreds of cat photos taken to retrain a new model that can differentiate  cats. Bounding box data will be available from the initial cat detector algorithm. Combine this with some input from the user that tags photos with the name of the cat found and that should be enough data required to train something like [yolov5](https://github.com/ultralytics/yolov5). This new model could then be used to customise feeds for each individual cat.

---

### [See the repo on GitHub ](https://github.com/eoinfennessy/clever-cat)
