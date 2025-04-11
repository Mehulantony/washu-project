<a name = "Pg1"></a>

# **Chapter 1** - Overview & Getting Started with Certifier Framework 

## 1.1 Purpose of the Lab
The Certifier Framework enables trusted interactions between applications and platforms by establishing and verifying security policies. It ensures compliance through key steps such as generating cryptographic keys, defining and signing policies, and provisioning these securely. 
The framework facilitates secure client-server communication by embedding trust at every level, from policy creation to application certification and runtime operations. Its setup involves building utilities, creating policies, provisioning files, and running trusted applications for secure services.

## 1.2 Prerequisites
The Certifier Framework for Confidential Computing is an open-source initiative designed to simplify and standardize the development and deployment of secure applications across diverse hardware platforms. It comprises two main components:
*	Certifier API - A client-side library that offers a unified interface for developers, facilitating tasks such as attestation evaluation, secure storage, platform initialization, secret sharing, and the establishment of secure communication channels. This API abstracts the complexities associated with various hardware implementations, enabling developers to write applications that are portable across multiple confidential computing environments. 
*	Certifier Service - A server-based policy evaluation system that supports scalable, policy-driven trust management. It evaluates attestations and enforces security policies, ensuring that applications comply with defined trust requirements. This service aids in managing trust relationships within a security domain, facilitating the deployment and operation of confidential computing applications on a scale.

By providing these tools, the Certifier Framework addresses several challenges inherent in confidential computing, including the diversity of hardware platforms, the complexity of security code implementation, and the need for scalable trust management solutions. It enables organizations to develop and deploy secure applications more efficiently, promoting the broader adoption of confidential computing practices.

In this lab, we will guide you through setting up the Certifier Framework on your device. You will prepare the environment by generating cryptographic keys, creating a policy for trust management, and provisioning necessary files for secure communication. The setup involves building utilities, provisioning the Certifier Service, and compiling an example application. By the end of this lab, you will have a fully operational Certifier Framework setup ready for testing and exploration of its capabilities.

## 1.3 References to guide lab work
Please use the links below to learn the related information for this lab. 

* <a href = "https://blogs.vmware.com/opensource/2022/11/22/confidential-computing-part-1-tackling-challenges/">*Confidential Computing: Part 1, Tackling the Challenge of Multi-cloud, Distributed Security at Scale*</a> - An introduction to the concept of Confidential Computing, discussing challenges in securing data across multi-cloud environments and distributed systems. 
* <a href = "https://blogs.vmware.com/opensource/2022/12/01/confidential-computing-part-2-the-technical-bits/">*Confidential Computing: Part 2, Technical Bits*</a> - A deep dive into the technical aspects of Confidential Computing, exploring how trusted execution environments (TEEs) and other technologies enhance data security. 
* <a href="https://blogs.vmware.com/opensource/2022/12/08/confidential-computing-part-3-the-certifier-framework/">*Confidential Computing: Part 3, The Certifier Framework*</a> - An overview of the Certifier Framework, a tool designed to facilitate secure computing by verifying and managing trust in Confidential Computing environments. 
* <a href ="https://github.com/ccc-certifier-framework/certifier-framework-for-confidential-computing">*GitHub (Certifier Framework for Confidential Computing)*</a> - A repository containing the source code and documentation for the Certifier Framework, an open-source project aimed at enhancing security in Confidential Computing.
* <a href = "https://kubernetes.io/docs/reference/kubectl">*Docker*</a> - A technology for building and running applications based on containers within an operating system.
* <a href = "https://aws.amazon.com/">*AWS (Amazon Web Services)*</a> - A cloud platform that offers a variety of services, including storage, compute, and databases. AWS allows users to build and run applications on-demand.
## 1.4 Goals/Outcomes:
By the end of this lab module, you will be able to:

(i)	Understand Confidential Computing Concepts

* Explain the fundamentals of Confidential Computing and its role in securing multi-cloud and distributed environments.
* Understand the importance of trust establishment and policy enforcement in secure applications.

(ii) Set Up and Configure the Certifier Framework

* Successfully install and configure the Certifier Framework on their system.
* Generate cryptographic keys for secure communication.
* Define, sign, and provision security policies for trusted interactions.

(iii) Develop Secure Applications Using the Certifier API

* Utilize the Certifier API to enable attestation, secure storage, and trust management in applications.
* Abstract hardware complexities to make applications portable across different Confidential Computing environments.

(iv) Deploy and Manage Trusted Services

* Set up the Certifier Service to evaluate attestations and enforce security policies.
* Manage trust relationships and ensure compliance with defined security policies.

(v) Test and Validate Secure Communication

* Run example applications to demonstrate secure client-server interactions.
* Verify policy compliance through real-time attestations and trust evaluations.
