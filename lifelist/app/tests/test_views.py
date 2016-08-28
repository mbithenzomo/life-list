import time

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from api.models import Bucketlist, Item

# Set test variables for test users
test_fname = "Test"
test_lname = "User"
test_username = "mytestuser"
test_username2 = "mytestuser2"
test_email = "testuser@gmail.com"
test_email2 = "testuser2@gmail.com"
test_password = "testPASSWORD2016"
test_password2 = "testPASSWORD1234"

# Set variables for test bucket lists
test_bucketlist_title = "The List of Awesome"
test_bucketlist_title2 = "Knowledge Goals"
test_bucketlist_description = "Awesome things!"
test_bucketlist_description2 = "Things to learn"

# Set variables for test items
test_item_title = "Swim with dolphins"
test_item_title2 = "Visit all continents"
test_item_description = "Take a swim with the dolphins in Watamu"
test_item_description2 = "Within 5 years"


class CreateObjects(object):
    def create_user(self):
        """Create the test user"""
        User.objects.create_user(
            username=test_username,
            email=test_email,
            password=test_password)
        self.test_user = User.objects.all()[:1].get()
        return self.test_user

    def login_user(self):
        """Log in as the test user"""
        self.driver.get(
            '%s%s' % (self.live_server_url, "/")
        )
        self.driver.find_element_by_id(
            "login_username").send_keys(test_username)
        self.driver.find_element_by_id(
            "login_password").send_keys(test_password)
        self.driver.find_element_by_id(
            "login_button").click()

    def create_bucketlist(self):
        """Create the test bucket list"""
        self.test_bucketlist = Bucketlist.objects.create(
            title=test_bucketlist_title,
            description=test_bucketlist_description,
            created_by=self.test_user)
        self.b_title = "bucketlist_" + str(self.test_bucketlist.id) + \
            "_title"
        self.b_description = "bucketlist_" + str(self.test_bucketlist.id) + \
            "_description"
        self.b_items_count = "bucketlist_" + str(self.test_bucketlist.id) + \
            "_items_count"
        return self.test_bucketlist, self.b_title, self.b_description,
        self.b_items_count

    def get_bucketlist_page(self):
        bucketlist_page_url = "/bucketlists/" + str(self.test_bucketlist.slug)
        self.driver.get(
            '%s%s' % (self.live_server_url, bucketlist_page_url)
        )
        time.sleep(1)

    def create_item(self):
        """Create the test bucket list item"""
        self.test_item = Item.objects.create(
            title=test_item_title,
            description=test_item_description,
            bucketlist=self.test_bucketlist,
            created_by=self.test_user)
        self.i_title = "item_" + str(self.test_item.id) + "_title"
        self.i_description = "item_" + str(self.test_item.id) + "_description"
        return self.test_item, self.i_title, self.i_description


class LifeListViewsTest(StaticLiveServerTestCase, CreateObjects):

    def setUp(self):
        """Setup the test driver and create objects"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.create_user()
        self.create_bucketlist()
        self.create_item()
        self.driver.get(
            '%s%s' % (self.live_server_url, "/")
        )
        super(LifeListViewsTest, self).setUp()

    def test_login_required(self):
        """
        Test that user must be logged in to access dashboard.
        Unauthenticated access redirects to the authentication page.
        """
        self.driver.get(
            '%s%s' % (self.live_server_url, "/dashboard")
        )
        self.assertEqual(self.driver.current_url,
                         "http://localhost:8081/?next=/dashboard")

    def test_dashboard(self):
        """
        Test that logging in directs users to the dashboard
        """
        self.login_user()
        self.driver.implicitly_wait(30)
        self.assertEqual(self.driver.current_url,
                         "http://localhost:8081/dashboard")
        time.sleep(1)
        dashboard_username = self.driver.find_element_by_id(
            "dashboard_username").text
        assert test_username.upper() in dashboard_username

    def test_bucketlist_display(self):
        """
        Test that bucket list is displayed on dashboard with the correct
        information
        """
        self.login_user()
        time.sleep(1)
        bucketlist_title = self.driver.find_element_by_id(
            self.b_title).text
        self.assertEqual(test_bucketlist_title.upper(), bucketlist_title)
        bucketlist_description = self.driver.find_element_by_id(
            self.b_description).text
        assert test_bucketlist_description in bucketlist_description
        items_count = self.driver.find_element_by_id(
            self.b_items_count).text
        assert "Number of Items: 1" in items_count

    def test_bucketlist_page(self):
        """
        Test that the bucket list page shows bucket list details as well as
        its bucket list items
        """
        self.login_user()
        bucketlist_page_url = "/bucketlists/" + str(self.test_bucketlist.slug)
        self.driver.get(
            '%s%s' % (self.live_server_url, bucketlist_page_url)
        )
        time.sleep(1)
        page_title = self.driver.find_element_by_id(
            "bucketlist_page_title").text
        assert test_bucketlist_title.upper() in page_title
        item_title = self.driver.find_element_by_id(
            self.i_title).text
        assert test_item_title in item_title
        item_description = self.driver.find_element_by_id(
            self.i_description).text
        assert test_item_description in item_description

    def tearDown(self):
        self.driver.quit()
        super(LifeListViewsTest, self).tearDown()


class AuthTest(StaticLiveServerTestCase):

    def setUp(self):
        """Setup the test driver"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(
            '%s%s' % (self.live_server_url, "/")
        )
        time.sleep(1)
        super(AuthTest, self).setUp()

    def user_registration(self):
        """
        Fills in the non-unique and non-validated
        fields of the registration form
        """
        self.driver.find_element_by_id(
            "register-tab").click()
        self.driver.find_element_by_id(
            "register_fname").send_keys(test_fname)
        self.driver.find_element_by_id(
            "register_lname").send_keys(test_lname)
        self.driver.find_element_by_id(
            "register_password").send_keys(test_password)

    def test_user_registration(self):
        """
        Test user registration with correct fields
        """
        # Register user
        self.user_registration()
        self.driver.find_element_by_id(
            "register_conf_password").send_keys(test_password)
        self.driver.find_element_by_id(
            "register_username").send_keys(test_username)
        self.driver.find_element_by_id(
            "register_email").send_keys(test_email)
        self.driver.find_element_by_id(
            "register_button").click()
        time.sleep(1)

        # Check for success message
        message = self.driver.find_element_by_id(
            "message-alerts").text
        assert "Successfully registered! Login to get started" in message

    def test_confirm_password(self):
        """
        Test that password and confirm_password fields must match
        """
        self.user_registration()
        # Enter non-matching password
        self.driver.find_element_by_id(
            "register_conf_password").send_keys(test_password2)
        self.driver.find_element_by_id(
            "register_username").send_keys(test_username)
        self.driver.find_element_by_id(
            "register_email").send_keys(test_email)
        self.driver.find_element_by_id(
            "register_button").click()
        time.sleep(1)

        # Check for error message
        message = self.driver.find_element_by_id(
            "message-alerts").text
        assert "Passwords do not match" in message

    def test_duplicate_email(self):
        """
        Test user registration with duplicate email
        """
        # Register first user
        self.test_user_registration()

        # Register second user with the same email
        self.user_registration()
        self.driver.find_element_by_id(
            "register_conf_password").send_keys(test_password)
        self.driver.find_element_by_id(
            "register_username").send_keys(test_username2)
        self.driver.find_element_by_id(
            "register_email").send_keys(test_email)
        self.driver.find_element_by_id(
            "register_button").click()
        time.sleep(1)

        # Check for error message
        message = self.driver.find_element_by_id(
            "message-alerts").text
        assert "That email address is already in use" in message

    def test_duplicate_username(self):
        """
        Test user registration with duplicate username
        """
        # Register first user
        self.test_user_registration()

        # Register second user with the same username
        self.user_registration()
        self.driver.find_element_by_id(
            "register_conf_password").send_keys(test_password)
        self.driver.find_element_by_id(
            "register_username").send_keys(test_username)
        self.driver.find_element_by_id(
            "register_email").send_keys(test_email2)
        self.driver.find_element_by_id(
            "register_button").click()
        time.sleep(1)

        # Check for error message
        message = self.driver.find_element_by_id(
            "message-alerts").text
        assert "A user with that username already exists" in message

    def test_login_wrong_credentials(self):
        """
        Test user login with incorrect username or password
        """
        # Register user
        self.test_user_registration()

        # Login with wrong password
        self.driver.find_element_by_id(
            "login_username").send_keys(test_username)
        self.driver.find_element_by_id(
            "login_password").send_keys(test_password2)
        self.driver.find_element_by_id(
            "login_button").click()
        time.sleep(1)

        # Check for error message
        message = self.driver.find_element_by_id(
            "message-alerts").text
        assert "Incorrect username or password" in message

        # Login with wrong username
        self.driver.find_element_by_id(
            "login_username").send_keys(test_username2)
        self.driver.find_element_by_id(
            "login_password").send_keys(test_password)
        self.driver.find_element_by_id(
            "login_button").click()
        time.sleep(1)

        # Check for error message
        message = self.driver.find_element_by_id(
            "message-alerts").text
        assert "Incorrect username or password" in message

    def tearDown(self):
        self.driver.quit()
        super(AuthTest, self).tearDown()


class BucketlistTest(StaticLiveServerTestCase, CreateObjects):

    def setUp(self):
        """Setup the test driver and create initial objects"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(
            '%s%s' % (self.live_server_url, "/")
        )
        self.create_user()
        self.login_user()
        time.sleep(1)
        super(BucketlistTest, self).setUp()

    def test_no_bucketlists(self):
        """
        Test that appropriate message is displayed when there are
        no bucket lists to display
        """
        message = self.driver.find_element_by_id(
            "no-bucketlists-message").text
        assert "Looks like you haven't added a bucket list yet" in message

    def test_add_bucketlist(self):
        """Test addition of a bucket list"""
        self.driver.find_element_by_id(
            "add-bucketlist-menu-link").click()
        time.sleep(1)

        self.driver.find_element_by_id(
            "add-bucketlist-title").send_keys(test_bucketlist_title)
        self.driver.find_element_by_id(
            "add-bucketlist-description").send_keys(test_bucketlist_description)
        self.driver.find_element_by_id(
            "add-bucketlist-button").click()
        time.sleep(1)

        # Confirm addition
        self.assertEqual(Bucketlist.objects.count(), 1)
        self.test_bucketlist = Bucketlist.objects.all()[:1].get()

    def delete_bucketlist_and_confirm(self):
        # Delete bucket list
        time.sleep(1)
        self.driver.find_element_by_id(
            "delete-bucketlist-button").click()
        time.sleep(1)

        # Confirm deletion
        self.assertEqual(Bucketlist.objects.count(), 0)

    def test_delete_bucketlist_dashboard(self):
        """Test deletion of bucket list from dashboard"""
        # Add bucket list
        self.test_add_bucketlist()

        # Open delete modal
        delete_link_dashboard = "delete_bucketlist_" + \
            str(self.test_bucketlist.id)
        self.driver.find_element_by_id(
            delete_link_dashboard).click()

        self.delete_bucketlist_and_confirm()

    def test_delete_bucketlist_page(self):
        """Test deletion of bucket list from bucket list page"""
        # Add bucket list
        self.test_add_bucketlist()

        # Open delete modal
        bucketlist_page_url = "/bucketlists/" + str(self.test_bucketlist.slug)
        self.driver.get(
            '%s%s' % (self.live_server_url, bucketlist_page_url)
        )
        time.sleep(1)
        self.driver.find_element_by_id(
            "delete-bucketlist-menu-link").click()

        self.delete_bucketlist_and_confirm()

    def edit_bucketlist_and_confirm(self):
        """Edit bucket list and confirm edit"""
        time.sleep(1)

        # Clear existing data
        self.driver.find_element_by_id(
            "edit-bucketlist-title").clear()
        self.driver.find_element_by_id(
            "edit-bucketlist-description").clear()

        # Add edit data
        self.driver.find_element_by_id(
            "edit-bucketlist-title").send_keys(
                test_bucketlist_title2)
        self.driver.find_element_by_id(
            "edit-bucketlist-description").send_keys(
                test_bucketlist_description2)
        self.driver.find_element_by_id(
            "edit-bucketlist-button").click()
        time.sleep(1)

        # Confirm edit
        title = "bucketlist_" + str(self.test_bucketlist.id) + \
            "_title"
        description = "bucketlist_" + str(self.test_bucketlist.id) + \
            "_description"
        bucketlist_title = self.driver.find_element_by_id(
            title).text
        self.assertEqual(test_bucketlist_title2.upper(), bucketlist_title)
        bucketlist_description = self.driver.find_element_by_id(
            description).text
        self.assertEqual(test_bucketlist_description2, bucketlist_description)

    def test_edit_bucketlist_dashboard(self):
        """Test editing of bucket list from dashboard"""
        # Add bucket list
        self.test_add_bucketlist()

        # Open edit modal
        edit_link_dashboard = "edit_bucketlist_" + \
            str(self.test_bucketlist.id)
        self.driver.find_element_by_id(
            edit_link_dashboard).click()

        self.edit_bucketlist_and_confirm()

    def test_edit_bucketlist_page(self):
        """Test editing of bucket list from bucket list page"""
        # Add bucket list
        self.test_add_bucketlist()

        # Open edit modal
        bucketlist_page_url = "/bucketlists/" + str(self.test_bucketlist.slug)
        self.driver.get(
            '%s%s' % (self.live_server_url, bucketlist_page_url)
        )
        time.sleep(1)
        self.driver.find_element_by_id(
            "edit-bucketlist-menu-link").click()

        self.edit_bucketlist_and_confirm()

    def tearDown(self):
        self.driver.quit()
        super(BucketlistTest, self).tearDown()


class ItemTest(StaticLiveServerTestCase, CreateObjects):

    def setUp(self):
        """Setup the test driver and create initial objects"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(
            '%s%s' % (self.live_server_url, "/")
        )
        self.create_user()
        self.create_bucketlist()
        self.login_user()
        time.sleep(1)
        super(ItemTest, self).setUp()

    def test_no_items(self):
        """
        Test that appropriate message is displayed when there are
        no items to display
        """
        self.login_user()
        self.get_bucketlist_page()
        message = self.driver.find_element_by_id(
            "no-items-message").text
        assert "Looks like you haven't added an item to this bucket list yet" \
            in message

    def add_item_and_confirm(self):
        time.sleep(1)
        self.driver.find_element_by_id(
            "add-item-title").send_keys(test_item_title)
        self.driver.find_element_by_id(
            "add-item-description").send_keys(test_item_description)
        self.driver.find_element_by_id(
            "add-item-button").click()
        time.sleep(1)

        # Confirm addition
        self.assertEqual(Item.objects.count(), 1)

    def test_add_item_dashboard(self):
        """Test addition of item from dashboard"""
        # Open add item modal
        add_item_link_dashboard = "add_item_bucketlist_" + \
            str(self.test_bucketlist.id)
        self.driver.find_element_by_id(
            add_item_link_dashboard).click()

        self.add_item_and_confirm()

    def test_add_item_page(self):
        """Test addition of item from bucket list page"""
        self.get_bucketlist_page()

        # Open add item modal
        self.driver.find_element_by_id(
            "add-item-menu-link").click()

        self.add_item_and_confirm()

    def test_edit_item(self):
        """Test editing of item"""
        self.test_add_item_page()
        self.get_bucketlist_page()

        # Open edit item modal
        test_item = Item.objects.all()[:1].get()
        edit_item_link = "edit_item_" + str(test_item.id)
        self.driver.find_element_by_id(
            edit_item_link).click()
        time.sleep(1)

        # Clear existing data
        self.driver.find_element_by_id(
            "edit-item-title").clear()
        self.driver.find_element_by_id(
            "edit-item-description").clear()

        # Add edit data
        self.driver.find_element_by_id(
            "edit-item-title").send_keys(test_item_title2)
        self.driver.find_element_by_id(
            "edit-item-description").send_keys(test_item_description2)
        self.driver.find_element_by_id(
            "edit-item-button").click()
        time.sleep(1)

        # Confirm edit
        title = "item_" + str(test_item.id) + \
            "_title"
        description = "item_" + str(test_item.id) + \
            "_description"
        item_title = self.driver.find_element_by_id(
            title).text
        self.assertEqual(test_item_title2, item_title)
        item_description = self.driver.find_element_by_id(
            description).text
        self.assertEqual(test_item_description2, item_description)

    def tearDown(self):
        self.driver.quit()
        super(ItemTest, self).tearDown()
