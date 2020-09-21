# To be reviewed by Eric 

## 1: New User Setup

0) If you haven't linked your LEAP account with your TXSTATE's github account then create an SSH key on your LEAP login node and link it to Texas State's github. Following the guides in the links below:
   
   Follow the steps in the link below to create a new SSH key (Note: In step 0 in the following link make sure you are logged onto LEAP): [generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent](https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
   
   Note: Make sure you have the linux tab selected for all instructions, unless done locally. 
   
   
   The following link below is nested in step 3 of the link above (Note: Step 1 might not work so use the command below to open file in a text editor to copy): [adding-a-new-ssh-key-to-your-github-account](https://help.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account)
    
   > vim ~/.ssh/id_rsa.pub
   

1) Clone graphB repository into some directory using the SSH link. If you are cloniong graphB on a local drive then clone repository using the HTTPS link.

   Example: home/user1/graphB

2) Clone any / all dataset repositories under the same parent directory as graphB (i.e. graphB and data-NAME are in the same directory).

   Example:   home/user1/graphB
              home/user1/data-NAME

3) Navigate and change directories to graphB/ and install the dependencies by entering the following commands in terminal.

   3.1) Install miniconda:

      Get Miniconda and make it the main Python interpreter. 
      Enter the following commands in terminal:

      > wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh

      > bash ~/miniconda.sh -b -p ~/miniconda 

      > rm ~/miniconda.sh

      > export PATH=~/miniconda/bin:$PATH

   3.2) Create a virtual environment
      
      Enter the following commands in terminal:

      > conda env create -f leap_env.yml
      
      After conda finishes setting up all packages you may get error saying:  
      
      > ERROR: Cannot uninstall 'PyYAML'. It is a distutils installed project and  
      > thus we cannot accurately determine which files belong to it... etc.  
               
      If you do get this error, your environment should have still been created.  
      
      Note: If any other package specific error occurs while creating environment, 
      then try commenting out any unneccessary packages that are causing the error.  
      
      To verify the environment still got created, run command: 
      
      > conda env list
      
      You should see the cam environment listed here.  
      
      After environment has been created,type the line:
      
      > conda init --all 
      
      **Close the terminal to apply changes.**
                 
      After opening new terminal, run commands:  
      
      > conda activate cam  
      > pip install --ignore-installed pyyaml

4) Go to home directory. Configure LEAP server by typing in the following lines of code:

   > wget http://apache.mirrors.lucidnetworks.net/spark/spark-2.3.4/spark-2.3.4-bin-hadoop2.7.tgz

   > tar xvf spark-2.3.4-bin-hadoop2.7.tgz

5) Copy the template files/folders and edit them as appropriate. 

   5.0) Navigate and change directories to graphB.
   
   5.1) The following is comprehensive list of directories/files you should copy:

      > cp -r configs_template/ configs/

      > cp preprocess/template_preprocess_general.sh preprocess/preprocess_general.sh 

      > cp process/template_process_general.sh process/process_general.sh

      > cp process/template_process_general_spark.sh process/process_general_spark.sh

      > cp postprocess/template_postprocess_general.sh postprocess/postprocess_general.sh

   5.2) In the following files, change lines of Josh's netID to users' netID, change miniconda3 to miniconda,
        and ensure the spark version matches the one you installed in "process_general_spark.sh".
       
      > vi postprocess/postprocess_general.sh

      > vi process/process_general_spark.sh

      > vi process/process_general.sh

      > vi preprocess/preprocess_general.sh
      
   5.3) Add empty slurmout directory
   
      > mkdir slurmout
  
 6) On GitHub, navigate to the Tutorial repository and continue the New User Setup.      
      
      
## 2: Usage

### 2.0: Initial Setup for each project

The following is for new analysis!

1) Raw_Data
   
   1.1) Create a directory labeled data-NAME that is in the same directory as graphB. NAME is the project name for the data.
   
   1.2) Navigate into the data-NAME directory and create a Raw_Data directory.
   
   1.3) Paste the user.csv and edges.csv into the Raw_Data directory.

**Note: As of 5/31/20 any 0.yaml file you use must include all parameters that are in the template copy [here](https://git.txstate.edu/DataLab/graphB/blob/master/configs_template/0.yaml)**

2) Configuration file (0.yaml file)

   2.1) Navigate and change directory to graphB/configs and create a directory with the NAME of the project for the data.
   
   e.g graphB/configs/NAME -> graphB/configs/ABCD
   
   2.2) Navigate into that newly created project directory and create a directory for the first label for your data. If no label, call the directory regular. 
   
   e.g graphB/configs/NAME/firstLabel -> graphB/configs/ABCD/Interview
      
   2.3) Navigate into that first label directory and create another directory for the second label of your data. If no label, call the directory regular.
   
   e.g graphB/configs/NAME/firstLabel/secondLabel -> graphB/configs/ABCD/Interview/1
   
   2.4) Navigate back to the root of the config directory. In that directory to copy the 0.yaml config file, and place it in the directory just created for the new data.
   
   e.g. > cp graphB/configs/example1/regular/regular/0.yaml graphB/configs/ABCD/Interview/1/

   Note: If you are copying from a local drive to a shell, or a shell to another shell the copying process might need more information. 

### 2.1: How to run the software

1) Navigate and change directories to graphB/

2) Type the following command into terminal to activate environment

   > conda activate cam
   
4) Type the following command into terminal 
   
   > python run.py
   
   - This will give you a list of the indexes for each configuration file availiable.
   - These config files are .yml files that have parameter settings that will govern what will happen when you run run.py. 
   - You can configure exactly what steps you want to do and where. 
   - For example, you can only perform the preprocessing step, or if you have already peformed the preprocessing step, you can decided to skip it and make trees with what you have preprocessed.
   Note: Each time you make trees, they will be added to the previous trees made. They do not overide each other, only concatinate.
   
5) Once you have selected the parameters in the configuration file type: 
   
   > python run.py 'index' 
   
   - Where 'index' is the index that matches your config file.
   
### 2.2: High memory node

The high memory node can be called upon when running the process with the parameter setting machine: "LEAP". 

The high memory node can be set for any of the 3 processess. However, the Process is the only part where the high memeory setting
should be set. 

The high memory node is a luxury setting that should not be taken advantage of. 

To call the high memory follow the following steps:

0) Make sure the configuration file has the parameter setting          

   machine: "LEAP"

1) Navigate and change directories into ~/graphB/process/ 

2) Run the following command

   > vim process_wrapper.py
   
3) Edit replace the old commands in the shell script by changing the following lines

   #SBATCH --partition=himem
   
   #SBATCH --mem=240G

4) Navigate and change directory back into graphB and run the process as usual.

   python run.py 'index'
   

## 3: Data 

### 3.1: Raw_Data

- The Raw_Data directory will primarily consist of two types of csv files.
- The users.csv file maps the Node_ID to the User_ID and may contain Labels. 
- The edges.csv file consists of three columns. "From_Node_ID", "To_Node_ID", "Edge_Weight"
- Note: No 0 Edge_Weight should be in edges.csv

users.csv example without labels:  
  
  Node ID, User ID
  
  0,R1
  
  1,R2
  
  2,R3
  
  ..

users.csv example with labels:  
  
  Node ID, User ID, Labels
  
  0,R1,1
  
  1,R2,0
  
  2,R3,1
  
  ...

edges.csv example:  
  
  From Node ID, To Node ID, Edge Weight
  
  0,1,-1
  
  0,2,-1
  
  1,2,1
  
  ...

### 3.2: Input_Data   

- Requires Raw_Data
- Before any analysis can be done, the raw data (csv) has to be converted into its matrix h5 format. 
- This is the Input Data step. For every connected component (CC) of your data above ~25 vertices, (ordered from highest to lowest, so 0.h5 is the highest CC of your data), there are two h5 files: 
- The symmetricized matrix
- The assymetric matrix.

- The symmetric matrix will be used to generate trees and balanced matrices. 
- The assymmetric matrix is used for degree analysis (i.e. in/out degree histograms) as part of Output Data.


### 3.3: Data

- Requires Input_Data
- When we refer to Data, we specifically mean h5 files containing balanced versions of a data set as well as the trees used to do perform the specific balancing. 
- Once this data is generated, the files will not be overwritten.


### 3.4: Output_Data

- Requires Data
- Plots, dataframes, statistics, tables, etc. as a result of analyzing the Data



## 4: Updating Dataset Respository 

### 4.1: Cloning new Dataset

- The most efficient is to clone you dataset repository after it is set up on Github
   - Put the Raw_Data directory in you dataset repository along with the users and edges csv files
   - Clone the data-DATASETNAME onto leap at the same level as other datasets and GraphB
   
### 4.2: After running GraphB

Nomatter if you have run the pre, post, or process potion of the software, it is good pactive push the latest updates back to Git! The steps to perform this are:

1) Navigate to the specific directory where tne new files are made.

2) In the command line type:

   >> git add _____   
      
      - where _____ is a file or directory. 
      
      Then
   
   >> git commit -m "note"
      
      - where "note" is a description of the file/directory you are pushing
   
   >> git push origin 
   
3) Check on Github that new files have been pushed, commited, or, merged. 

   
