from django.db import models
from django.utils.html import format_html
# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class City(models.Model):
    inst = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class TrainingData(models.Model):
    reg_id=models.IntegerField()
    array=models.BinaryField()

    def __str__(self):
      return str(self.pk)+" "+str(self.reg_id)

class Holidays(models.Model):
    year=models.IntegerField()
    month=models.CharField(max_length=15)
    day=models.CharField(max_length=80)

    def __str__(self):
      return str(self.pk)+" "+str(self.year)+" "+str(self.month)+" "+str(self.day)


class Attendance(models.Model):
    reg_id=models.IntegerField()
    inst=models.CharField(max_length=10)
    dept=models.CharField(max_length=10)
    date=models.DateField(null=True,blank=True)
    in_time=models.TimeField(blank=True,null=True)
    out_time=models.TimeField(blank=True,null=True)
    total_hour=models.FloatField(blank=True,null=True)
    is_status=models.BooleanField(default=False)

    is_leave=models.BooleanField(default=False)
    type_leave=models.CharField(max_length=20,null=True)
    shift_leave=models.CharField(max_length=20,null=True)

    def __str__(self):
        return str(self.pk)+" "+str(self.reg_id)+" "+str(self.inst)+" "+str(self.dept)+" "+str(self.date)+" "+str(self.in_time)+" "+str(self.out_time)+" "+str(self.total_hour)+" "+str(self.is_status)+" "+str(self.is_leave)+" "+str(self.type_leave)+" "+str(self.shift_leave)

class Person(models.Model):
    fname=models.CharField(max_length=20,null=True)
    lname=models.CharField(max_length=20,null=True)
    email=models.EmailField(max_length=50,null=True)
    password=models.CharField(max_length=100,blank=True,null=True)
    reg_id=models.IntegerField(blank=True,null=True)
    inst = models.ForeignKey(Country, on_delete=models.SET_NULL,blank=True, null=True)
    dept = models.ForeignKey(City, on_delete=models.SET_NULL,blank=True, null=True)
    is_pass_change=models.BooleanField(blank=True,null=True,default=True)


    def __str__(self):
        # print("inside model str :: institute is -->",self.inst," and department is -->",self.dept)
        # print("Boolean value is : ",( (str(self.inst) == 'DEPSTAR') and (str(self.dept) == 'CSE') ) )
        if str(self.inst) is "CSPIT" and str(self.dept) is "CE":
            return format_html('''
<tr><th><label for="id_fname">First Name:</label></th><td><input type="text" value="'''+str(self.fname)+'''" name="fname" class="form-control" maxlength="20" required id="id_fname"></td></tr>
<tr><th><label for="id_lname">Last Name:</label></th><td><input type="text" value="'''+str(self.lname)+'''" name="lname" class="form-control" maxlength="20" required id="id_lname"></td></tr>
<tr><th><label for="id_email">Email:</label></th><td><input type="email" value="'''+str(self.email)+'''" name="email" class="form-control" maxlength="20" required id="id_email" readonly></td></tr>
<tr><th><label for="id_reg_id">Employee id:</label></th><td><input type="number" value="'''+str(self.reg_id)+'''" name="reg_id" id="id_reg_id" readonly></td></tr>
<tr><th><label for="id_inst">Institute:</label></th><td><select name="inst" value="'''+str(self.inst)+'''" id="id_inst">
  <option value="0" disabled='true'>-----</option>
  <option value="1" selected>CSPIT</option> 
  <option value="2" >DEPSTAR</option>

</select></td></tr>
<tr><th><label for="id_dept">Department:</label></th><td><select name="dept" value="'''+str(self.dept)+'''" id="id_dept">
  <option value="0" disabled='true'>----</option>
  <option value="1" selected>CE</option>

  <option value="2">IT</option>

  <option value="3">CE</option>

  <option value="4">CSE</option>

  <option value="5">IT</option>

</select><input type="hidden" name="password" value="'''+str(self.password)+'''" id="id_password"></td></tr>
        ''')

        elif str(self.inst) is "CSPIT" and str(self.dept) is "IT":
             return format_html('''
<tr><th><label for="id_fname">First Name:</label></th><td><input type="text" value="'''+str(self.fname)+'''" name="fname" class="form-control" maxlength="20" required id="id_fname"></td></tr>
<tr><th><label for="id_lname">Last Name:</label></th><td><input type="text" value="'''+str(self.lname)+'''" name="lname" class="form-control" maxlength="20" required id="id_lname"></td></tr>
<tr><th><label for="id_email">Email:</label></th><td><input type="email" value="'''+str(self.email)+'''" name="email" class="form-control" maxlength="20" required id="id_email" readonly></td></tr>
<tr><th><label for="id_reg_id">Employee id:</label></th><td><input type="number" value="'''+str(self.reg_id)+'''" name="reg_id" id="id_reg_id" readonly></td></tr>
<tr><th><label for="id_inst">Institute:</label></th><td><select name="inst" value="'''+str(self.inst)+'''" id="id_inst">
  <option value="0" disabled='true'>-----</option>
  <option value="1" selected>CSPIT</option> 
  <option value="2" >DEPSTAR</option>

</select></td></tr>
<tr><th><label for="id_dept">Department:</label></th><td><select name="dept" value="'''+str(self.dept)+'''" id="id_dept">
  <option value="0" disabled='true'>----</option>
  <option value="1" >CE</option>

  <option value="2" selected>IT</option>

  <option value="3">CE</option>

  <option value="4">CSE</option>

  <option value="5">IT</option>

</select><input type="hidden" name="password" value="'''+str(self.password)+'''" id="id_password"></td></tr>
        ''')

        elif str(self.inst) is "DEPSTAR" and str(self.dept) is "CE":
            return format_html('''
<tr><th><label for="id_fname">First Name:</label></th><td><input type="text" value="'''+str(self.fname)+'''" name="fname" class="form-control" maxlength="20" required id="id_fname"></td></tr>
<tr><th><label for="id_lname">Last Name:</label></th><td><input type="text" value="'''+str(self.lname)+'''" name="lname" class="form-control" maxlength="20" required id="id_lname"></td></tr>
<tr><th><label for="id_email">Email:</label></th><td><input type="email" value="'''+str(self.email)+'''" name="email" class="form-control" maxlength="20" required id="id_email" readonly></td></tr>
<tr><th><label for="id_reg_id">Employee id:</label></th><td><input type="number" value="'''+str(self.reg_id)+'''" name="reg_id" id="id_reg_id" readonly></td></tr>
<tr><th><label for="id_inst">Institute:</label></th><td><select name="inst" value="'''+str(self.inst)+'''" id="id_inst">
  <option value="0" disabled='true'>-----</option>
  <option value="1" >CSPIT</option> 
  <option value="2" selected>DEPSTAR</option>

</select></td></tr>
<tr><th><label for="id_dept">Department:</label></th><td><select name="dept" value="'''+str(self.dept)+'''" id="id_dept">
  <option value="0" disabled='true'>----</option>
  <option value="1" >CE</option>

  <option value="2" >IT</option>

  <option value="3" selected>CE</option>

  <option value="4">CSE</option>

  <option value="5">IT</option>

</select><input type="hidden" name="password" value="'''+str(self.password)+'''" id="id_password"></td></tr>
        ''')

        elif str(self.inst) == "DEPSTAR" and str(self.dept) == "CSE":
            return format_html('''
<tr><th><label for="id_fname">First Name:</label></th><td><input type="text" value="'''+str(self.fname)+'''" name="fname" class="form-control" maxlength="20" required id="id_fname"></td></tr>
<tr><th><label for="id_lname">Last Name:</label></th><td><input type="text" value="'''+str(self.lname)+'''" name="lname" class="form-control" maxlength="20" required id="id_lname"></td></tr>
<tr><th><label for="id_email">Email:</label></th><td><input type="email" value="'''+str(self.email)+'''" name="email" class="form-control" maxlength="20" required id="id_email" readonly></td></tr>
<tr><th><label for="id_reg_id">Employee id:</label></th><td><input type="number" value="'''+str(self.reg_id)+'''" name="reg_id" id="id_reg_id" readonly></td></tr>
<tr><th><label for="id_inst">Institute:</label></th><td><select name="inst" value="'''+str(self.inst)+'''" id="id_inst">
  <option value="0" disabled='true'>-----</option>
  <option value="1" >CSPIT</option> 
  <option value="2" selected>DEPSTAR</option>

</select></td></tr>
<tr><th><label for="id_dept">Department:</label></th><td><select name="dept" value="'''+str(self.dept)+'''" id="id_dept">
  <option value="0" disabled='true'>----</option>
  <option value="1" >CE</option>

  <option value="2" >IT</option>

  <option value="3">CE</option>

  <option value="4" selected>CSE</option>

  <option value="5">IT</option>

</select><input type="hidden" name="password" value="'''+str(self.password)+'''" id="id_password"></td></tr>
        ''')

        elif str(self.inst) is "DEPSTAR" and str(self.dept) is "IT":
            return format_html('''
<tr><th><label for="id_fname">First Name:</label></th><td><input type="text" value="'''+str(self.fname)+'''" name="fname" class="form-control" maxlength="20" required id="id_fname"></td></tr>
<tr><th><label for="id_lname">Last Name:</label></th><td><input type="text" value="'''+str(self.lname)+'''" name="lname" class="form-control" maxlength="20" required id="id_lname"></td></tr>
<tr><th><label for="id_email">Email:</label></th><td><input type="email" value="'''+str(self.email)+'''" name="email" class="form-control" maxlength="20" required id="id_email" readonly></td></tr>
<tr><th><label for="id_reg_id">Employee id:</label></th><td><input type="number" value="'''+str(self.reg_id)+'''" name="reg_id" id="id_reg_id" readonly></td></tr>
<tr><th><label for="id_inst">Institute:</label></th><td><select name="inst" value="'''+str(self.inst)+'''" id="id_inst">
  <option value="0" disabled='true'>-----</option>
  <option value="1" >CSPIT</option> 
  <option value="2" selected>DEPSTAR</option>
 
</select></td></tr>
<tr><th><label for="id_dept">Department:</label></th><td><select name="dept" value="'''+str(self.dept)+'''" id="id_dept">
  <option value="0" disabled='true'>----</option>
  <option value="1" >CE</option>

  <option value="2">IT</option>

  <option value="3">CE</option>

  <option value="4">CSE</option>

  <option value="5" selected>IT</option>

</select><input type="hidden" name="password" value="'''+str(self.password)+'''" id="id_password"></td></tr>
        ''')

        else:
            return format_html('''
<tr><th><label for="id_fname">First Name:</label></th><td><input type="text" value="'''+str(self.fname)+'''" name="fname" class="form-control" maxlength="20" required id="id_fname"></td></tr>
<tr><th><label for="id_lname">Last Name:</label></th><td><input type="text" value="'''+str(self.lname)+'''" name="lname" class="form-control" maxlength="20" required id="id_lname"></td></tr>
<tr><th><label for="id_email">Email:</label></th><td><input type="email" value="'''+str(self.email)+'''" name="email" class="form-control" maxlength="20" required id="id_email" readonly></td></tr>
<tr><th><label for="id_reg_id">Employee id:</label></th><td><input type="number" value="'''+str(self.reg_id)+'''" name="reg_id" id="id_reg_id" readonly></td></tr>
<tr><th><label for="id_inst">Institute:</label></th><td><select name="inst" value="'''+str(self.inst)+'''" id="id_inst">
  <option value="0" disabled='true' selected>-----</option>
  <option value="1" >CSPIT</option> 
  <option value="2">DEPSTAR</option>

</select></td></tr>
<tr><th><label for="id_dept">Department:</label></th><td><select name="dept" value="'''+str(self.dept)+'''" id="id_dept">
  <option value="0" disabled='true' selected>----</option>
  <option value="1" >CE</option>

  <option value="2">IT</option>

  <option value="3">CE</option>

  <option value="4">CSE</option>

  <option value="5">IT</option>

</select><input type="hidden" name="password" value="'''+str(self.password)+'''" id="id_password"></td></tr>
        ''')
            

