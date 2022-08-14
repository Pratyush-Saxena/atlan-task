# atlan-task

[Problem Statement](https://docs.google.com/document/d/15hensnwWfZzxKkt6ybdFd6rM9WuzoylO-yYG-kH--KU/edit)

## Subtask 1
<p> Design a sample schematic for how you would store forms (with questions) and responses (with answers) in the Collect data store. Forms, Questions, Responses and Answers each will have relevant metadata.</p>

### Approach
<li> <b> Schema - </b> </li>

![Schema](https://user-images.githubusercontent.com/52444607/184525639-a303f5f1-9015-473a-a192-50285e473d56.png)

<li>
The above image shows the schematic approach of implementation.So as we can see that the tables itself stores the metadata of the form,For ex. field table have columns like 
 <ul>
 <li> type - type of data to be accepted in this field </li>
  <li> mandate - if the feild is mandatory or not</li>
  <li> upper_ limit and lower_limit - to add constraint to the input</li>
 </ul>
 and many more which can be check at the time of response submisson.
</li>

<li> APIs-
</li>

![127 0 0 1_5000_swagger-ui_](https://user-images.githubusercontent.com/52444607/184526244-d39f054e-11e2-4d23-a19c-da7214372b74.png)

<li>
These are the REST APIs implemented using <a href="https://flask-restful.readthedocs.io/en/latest/">flask-restful</a>, and are protected with JWT token based authentication.
</li>


## Subtask 2

<p>Design and implement a solution for the Google Sheets use case and choose any one of the others to keep in mind how we want to solve this problem in a plug-n-play fashion. Make fair assumptions wherever necessary.</p>

### Approach

<li>For googlesheet plugin, the service is designed seperately using <a href="https://developers.google.com/sheets/api/reference/rest" >GoogleSheet API</a>. </li>
https://github.com/Pratyush-Saxena/atlan-task/blob/3d5759cf47c0225efded267c9dfe667570554258/plugins/googlesheet/__init__.py#L4-L38

<li>So the Service can easily be called by initializing whenever needed</li>
https://github.com/Pratyush-Saxena/atlan-task/blob/3d5759cf47c0225efded267c9dfe667570554258/collect/routes.py#L139-L180

![docs google com_spreadsheets_d_1yNbMjl0F6F9YGEOTgi2MwgeuTWHuNr7w9TB-NMbI4QE_edit](https://user-images.githubusercontent.com/52444607/184526848-d119ad68-0b8e-4e60-9f8b-56a3197b4328.png)

## Getting Started
<ol>
<li>Clone the repository</li>

``` 
git clone https://github.com/Pratyush-Saxena/atlan-task.git
```
<li>Run docker-compose</li>

```
docker-compose up --build
```
<li> Open Url <ahref="" >http://127.0.0.1:5000/swagger-ui/#/default</a> </li>
