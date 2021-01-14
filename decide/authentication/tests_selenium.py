from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import time
import json
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from django.contrib.auth.models import User
from .models import VotingUser

from base.tests import BaseTestCase

class TestRegister(StaticLiveServerTestCase):
  def setUp(self):
    #Load base test functionality for decide
    self.base = BaseTestCase()
    self.base.setUp()

    options = webdriver.ChromeOptions()
    options.headless = True

    self.driver = webdriver.Chrome(options=options)

    super().setUp()

    u1 = User(username='voter1')
    u1.set_password('123')
    u1.save()

    u2 = User(username='voter2', email='voter2@gmail.com')
    u2.set_password('123')
    u2.save()
    vu2 = VotingUser(user=u2, dni='45454545T', sexo='Man', titulo='Software', curso='First', edad=18)
    vu2.save()      
            
  def tearDown(self):           
    super().tearDown()
    self.driver.quit()

    self.base.tearDown()
  
  def test_getRegisterAnonymous(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Register").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".container > h1").text == "REGISTER"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(3) > label").text == "Username:"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(4) > label").text == "Email address:"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(5) > label").text == "Password:"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(8) > label").text == "Password confirmation:"
    assert self.driver.find_element(By.CSS_SELECTOR, "h3:nth-child(9)").text == "Voting User"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(10) > label").text == "NIF:"
    value = self.driver.find_element(By.ID, "id_dni").get_attribute("value")
    assert value == ""
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(11) > label").text == "Gender:"
    value = self.driver.find_element(By.ID, "id_sexo").get_attribute("value")
    assert value == "Woman"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(12) > label").text == "Grade:"
    value = self.driver.find_element(By.ID, "id_titulo").get_attribute("value")
    assert value == "Software"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(13) > label").text == "Year:"
    value = self.driver.find_element(By.ID, "id_curso").get_attribute("value")
    assert value == "First"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(14) > label").text == "Candidature:"
    value = self.driver.find_element(By.ID, "id_candidatura").get_attribute("value")
    assert value == ""
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(15) > label").text == "Age:"
    value = self.driver.find_element(By.ID, "id_edad").get_attribute("value")
    assert value == "18"
    value = self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").get_attribute("value")
    assert value == "Submit"

  def test_getRegisterLoggedUserIncompleteProfile(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Login").click()
    self.driver.find_element(By.ID, "id_username").send_keys("voter1")
    self.driver.find_element(By.ID, "id_password").send_keys("123")
    self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
    assert self.driver.find_element(By.LINK_TEXT, "voter1").text == "voter1"
    assert self.driver.find_element(By.LINK_TEXT, "Finish setting your profile here to access the platform").text == "Finish setting your profile here to access the platform"
    self.driver.get(f'{self.live_server_url}/authentication/decide/register')
    assert self.driver.find_element(By.CSS_SELECTOR, ".container > h1").text == "REGISTER"
    assert self.driver.find_element(By.CSS_SELECTOR, "h3").text == "Voting User"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(3) > label").text == "NIF:"
    value = self.driver.find_element(By.ID, "id_dni").get_attribute("value")
    assert value == ""
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(4) > label").text == "Gender:"
    value = self.driver.find_element(By.ID, "id_sexo").get_attribute("value")
    assert value == "Woman"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(5) > label").text == "Grade:"
    value = self.driver.find_element(By.ID, "id_titulo").get_attribute("value")
    assert value == "Software"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(6) > label").text == "Year:"
    value = self.driver.find_element(By.ID, "id_curso").get_attribute("value")
    assert value == "First"
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(7) > label").text == "Candidature:"
    value = self.driver.find_element(By.ID, "id_candidatura").get_attribute("value")
    assert value == ""
    assert self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(8) > label").text == "Age:"
    value = self.driver.find_element(By.ID, "id_edad").get_attribute("value")
    assert value == "18"
    value = self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(9)").get_attribute("value")
    assert value == "Submit"
  
  def test_getRegisterLoggedUserCompleteProfile(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Login").click()
    self.driver.find_element(By.ID, "id_username").send_keys("voter2")
    self.driver.find_element(By.ID, "id_password").send_keys("123")
    self.driver.find_element(By.ID, "id_password").send_keys(Keys.ENTER)
    assert self.driver.find_element(By.LINK_TEXT, "voter2").text == "voter2"
    self.driver.get(f'{self.live_server_url}/authentication/decide/register')
    assert self.driver.find_element(By.CSS_SELECTOR, ".container > h1").text == "REGISTER"
    assert self.driver.find_element(By.CSS_SELECTOR, ".container li").text == "You are already registered."

  def test_registerCorrect(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Register").click()
    self.driver.find_element(By.ID, "id_username").send_keys("username1988")
    self.driver.find_element(By.ID, "id_email").send_keys("username1988@gmail.com")
    self.driver.find_element(By.ID, "id_password1").send_keys("password1234")
    self.driver.find_element(By.ID, "id_password2").send_keys("password1234")
    self.driver.find_element(By.ID, "id_dni").send_keys("48978965K")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").click()
    assert self.driver.find_element(By.LINK_TEXT, "username1988").text == "username1988"

  def test_registerEmptyFields(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Register").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".container > h1").text == "REGISTER"
    self.driver.find_element(By.ID, "id_email").send_keys("username1989@gmail.com")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".container > h1").text == "REGISTER"
    self.driver.find_element(By.ID, "id_username").send_keys("username1989")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".container > h1").text == "REGISTER"
    self.driver.find_element(By.ID, "id_password1").send_keys("pasword1234")
    self.driver.find_element(By.ID, "id_password2").send_keys("password1234")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".container > h1").text == "REGISTER"
    value = self.driver.find_element(By.ID, "id_dni").get_attribute("value")
    assert value == ""

  def test_registerDuplicatedDni(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Register").click()
    self.driver.find_element(By.ID, "id_username").send_keys("username1900")
    self.driver.find_element(By.ID, "id_email").send_keys("username1900@gmail.com")
    self.driver.find_element(By.ID, "id_password1").send_keys("password1234")
    self.driver.find_element(By.ID, "id_password2").send_keys("password1234")
    self.driver.find_element(By.ID, "id_dni").send_keys("45454545T")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").text == "Voting user with this NIF already exists."
  
  def test_registerDuplicatedEmail(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Register").click()
    self.driver.find_element(By.ID, "id_username").send_keys("username1900")
    self.driver.find_element(By.ID, "id_email").send_keys("voter2@gmail.com")
    self.driver.find_element(By.ID, "id_password1").send_keys("password1234")
    self.driver.find_element(By.ID, "id_password2").send_keys("password1234")
    self.driver.find_element(By.ID, "id_dni").send_keys("48978900K")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").text == "This email is already in use"
  
  def test_registerDuplicatedUsername(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Register").click()
    self.driver.find_element(By.ID, "id_username").send_keys("voter2")
    self.driver.find_element(By.ID, "id_email").send_keys("username1900@gmail.com")
    self.driver.find_element(By.ID, "id_password1").send_keys("password1234")
    self.driver.find_element(By.ID, "id_password2").send_keys("password1234")
    self.driver.find_element(By.ID, "id_dni").send_keys("48978900K")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").text == "A user with that username already exists."

  def test_registerDifferentPasswords(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Register").click()
    self.driver.find_element(By.ID, "id_username").send_keys("username1900")
    self.driver.find_element(By.ID, "id_email").send_keys("username1900@gmail.com")
    self.driver.find_element(By.ID, "id_password1").send_keys("password1234")
    self.driver.find_element(By.ID, "id_password2").send_keys("password4321")
    self.driver.find_element(By.ID, "id_dni").send_keys("48978900K")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").text == "The two password fields didn't match."

  def test_registerWrongPasswordFormat(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Register").click()
    self.driver.find_element(By.ID, "id_username").send_keys("username1900")
    self.driver.find_element(By.ID, "id_email").send_keys("username1900@gmail.com")
    self.driver.find_element(By.ID, "id_password1").send_keys("username1900")
    self.driver.find_element(By.ID, "id_password2").send_keys("username1900")
    self.driver.find_element(By.ID, "id_dni").send_keys("48978900K")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").text == "The password is too similar to the username."
    self.driver.find_element(By.ID, "id_password1").send_keys("pass12")
    self.driver.find_element(By.ID, "id_password2").send_keys("pass12")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(17)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").text == "This password is too short. It must contain at least 8 characters."
    self.driver.find_element(By.ID, "id_password1").send_keys("password")
    self.driver.find_element(By.ID, "id_password2").send_keys("password")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(17)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").text == "This password is too common."
    self.driver.find_element(By.ID, "id_password1").send_keys("87512396")
    self.driver.find_element(By.ID, "id_password2").send_keys("87512396")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(17)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").text == "This password is entirely numeric."

'''
#Input type number send keys is not supported in the web driver version
  def test_registerWrongAge(self):
    self.driver.get(f'{self.live_server_url}/')
    self.driver.set_window_size(1296, 696)
    self.driver.find_element(By.LINK_TEXT, "Register").click()
    self.driver.find_element(By.ID, "id_username").send_keys("username1900")
    self.driver.find_element(By.ID, "id_email").send_keys("username1900@gmail.com")
    self.driver.find_element(By.ID, "id_password1").send_keys("password1234")
    self.driver.find_element(By.ID, "id_password2").send_keys("password1234")
    self.driver.find_element(By.ID, "id_dni").send_keys("48978900K")
    self.driver.find_element(By.ID, "id_edad").send_keys("16")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(16)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist").text == "Ensure this value is greater than or equal to 17."
    self.driver.find_element(By.ID, "id_password1").send_keys("password1234")
    self.driver.find_element(By.ID, "id_password2").send_keys("password1234")
    self.driver.find_element(By.ID, "id_edad").send_keys("101")
    self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(17)").click()
    assert self.driver.find_element(By.CSS_SELECTOR, ".errorlist > li").text == "Ensure this value is less than or equal to 100."
'''
  
  