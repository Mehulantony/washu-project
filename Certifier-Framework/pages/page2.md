# **Chapter 2** - Preparation of Lab Environment 


<a name = "Pg2"></a>

<!--# **Chapter 2** - Preparation of Lab Environment-->

## 2.1 Instance Preparation

<blockquote style = "background-color: #e5f5e0 ; margin: 0 ; font-family: calibri;border: 2px solid #00441b; border-left: 6px solid #00441b; padding : 0.5em; border-radius: 8px; background-style:discrete" >
    <font size = 3 color = green> <b> Note: </b></font><font color = 'black'>
Operating System: Certifier Framework is designed to run in Linux environments. This is primarily because:

- System calls and dependencies: It relies on Linux-specific system interfaces and libraries (like libssl, libprotobuf, etc.).

- Build tools and scripts: The setup uses build tools like make, cmake, and dependencies typically installed via apt, which are native to Debian/Ubuntu or similar Linux distributions.

- Enclave Support: If you're working with Intel SGX enclaves, they require Linux for most development environments and SDK/tooling. </font> </blockquote>

* Go to AWS and Sign In. Start by visiting AWS Management Console in your web browser. If you already have an AWS account, sign in with your credentials.


* Selecting the AWS Region in the console home:

In the top-right corner of the AWS Management Console, click on the current region (e.g., "US-East-1"). A dropdown menu will appear listing various AWS regions. Select the preferred region for your EC2 instance - "N.Virginia".

<a name = "fig2.1"></a><img src = "../img/region+.png" align = "center"/></center>


* Navigating to the AWS EC2 Service:

In the search bar at the top, type "EC2". Click on the "EC2 - Virtual Servers in the Cloud" option from the dropdown menu to open the EC2 dashboard.

<center>
<a name = "fig2.1"></a><img src = "../img/sea2.png" align = "center"/></center>

* As a result to clicking E2C, it will take to this page where you willl select "AMIs" in the left side of the page to create your AWS Instance

<center>
<a name = "fig2.1"></a><img src = "../img/AMI_option.png" align = "center"/></center>

* Search AMIs, type: "certifier_fw_image" and select the AMI. Click "Launch instance from AMI" in the top right corner. Make sure to check the filter that it is "Public Images". It might take a minute to load. 

<center>
<a name = "fig2.1"></a><img src = "../img/over_AMI.png" align = "center"/></center>


## 2.2 Launch an Instance
Create your virtual instance 

<center>
<a name = "fig2.1"></a><img src = "../img/pcf.png" align = "center"/></center>


* Enter a unique name for your virtual machine (EC2 instance) under the "Name and tags" section.
* This name helps you identify your instance among multiple instances in your AWS environment.
* Example: In the image, the instance is named "sample_instance".

<center>
<a name = "fig2.1"></a><img src = "../img/Instance_name.png" align = "center"/></center>


* Make sure the Application and OS image is already configured to the selected AMI's settings.

<center>
<a name = "fig2.2"></a><img src = "../img/eact.png" align = "center"/></center>

<center>
<a name = "fig2.2"></a><img src = "../img/ty.png" align = "center"/></center>

* Create new Key Pair (login) 

<center>
<a name = "fig2.2"></a><img src = "../img/Key Pair.png" align = "center"/></center>

* Name your Key & create

<center>
<a name = "fig2.2"></a><img src = "../img/Name Key.png" align = "center"/></center>


<blockquote style = "background-color: #e5f5e0 ; margin: 0 ; font-family: calibri;border: 2px solid #00441b; border-left: 6px solid #00441b; padding : 0.5em; border-radius: 8px; background-style:discrete" >
    <font size = 3 color = green> <b> Note: </b></font><font color = 'black'>
The created key pair will be downloaded locally. </font> </blockquote>

* Make sure your Network settings and your storage configurations remain the same with no changes required. The existing configurations are from your selected AMI.

<center>
<a name = "fig2.5"></a><img src = "../img/chill.png" align = "center"/></center>


* On the left side of the portal, you can view your instance summary. ***Launch Instance***

<center>
<a name = "fig2.6"></a><img src = "../img/AMI_sum.png" align = "center"/></center>

<center>
<a name = "fig2.7"></a><img src = "../img/vera.png" align = "center"/></center>


* Below, choose the option: "connect to your instance"

<center>
<a name = "fig2.7"></a><img src = "../img/specific.png" align = "center"/></center>



<center>
<a name = "fig2.8"></a><img src = "../img/final_con.png" align = "center"/></center>


***Your AWS instance***

You might face a connection issue (NAT issue), reload your tab or relaunch your created instance. You will end up in this view as shown in the figure below.

<center>
<a name = "fig2.11"></a><img src = "../img/final_pah.png" align = "center"/></center>


