from gi.repository import Gtk, Adw, Gio, GLib

from envoye.classes.API import *
from envoye.classes.label import Label

@Gtk.Template(resource_path='/de/davidbattefeld/envoye/window.ui')
class EnvoyeWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'EnvoyeWindow'

    main_box = Gtk.Template.Child()
    api_test_button = Gtk.Template.Child()
    load_mails_test_button = Gtk.Template.Child()
    sidebar_list_box = Gtk.Template.Child()
    mail_body_box = Gtk.Template.Child()
    mail_teaser_list_box = Gtk.Template.Child()
    toast_overlay = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api = API()
        self.labels = []

        self.settings = Gio.Settings(schema_id="de.davidbattefeld.envoye")

        self.settings.bind("window-width", self, "default-width",
                       Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("window-height", self, "default-height",
                       Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("window-maximized", self, "maximized",
                       Gio.SettingsBindFlags.DEFAULT)

        api_test_action = Gio.SimpleAction(name="api_test")
        api_test_action.connect("activate", self.test_action)
        self.add_action(api_test_action)

        api_mails_inbox = Gio.SimpleAction(name="api_mails_inbox")
        api_mails_inbox.connect("activate", self.test_inbox_action)
        self.add_action(api_mails_inbox)

        load_emails_for_label = Gio.SimpleAction(
                name="load_emails_for_label", 
                #parameter_type=GLib.VariantType.new('s')
            )
        load_emails_for_label.connect("activate", self.load_emails_for_label)
        self.add_action(load_emails_for_label)

        self.load_labels()

        # load_labels_action = Gio.SimpleAction(name="load_labels")
        # load_labels_action.connect("activate", self.load_labels)
        # self.add_action(load_labels_action)

    def test_action(self, action, _):
        self.api.load_and_print_labels()
        self.toast_overlay.add_toast(Adw.Toast(title="Labels loaded and printed to console"))

    def test_inbox_action(self, action, _):
        self.api.load_messages_for_label("INBOX")

    def load_labels(self):
        loadedLabels = self.api.load_labels()
        if not loadedLabels:
            pass

        for item in loadedLabels:
            label = Label(item['id'], item['name'], item['type'])
            self.labels.append(label)

            text = Gtk.Label.new(label.name)
            box_row = Gtk.ListBoxRow()
            box_row.set_child(text)
            box_row.set_action_name('win.load_emails_for_label')
            #box_row.set_action_target(label.id)
            self.sidebar_list_box.append(box_row)

    def load_emails_for_label(self, action, _):
        label_id = 'INBOX'
        #self.mail_teaser_list_box.remove_all() #Apparently unstable and GTK 4.12
        messages = self.api.load_messages_for_label(labelIds=label_id) #TODO: pass value

        for message in messages:
            snippet = Gtk.Label.new(message.snippet)
            box_row = Gtk.ListBoxRow()
            box_row.set_child(snippet)
            self.mail_teaser_list_box.append(box_row)

        self.toast_overlay.add_toast(Adw.Toast(title=f"Refreshed emails for label {label_id}"))

class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'envoye'
        self.props.version = "0.1.0"
        self.props.authors = ['dbt']
        self.props.copyright = '2023 dbt'
        self.props.logo_icon_name = 'de.davidbattefeld.envoye'
        self.props.modal = True
        self.set_transient_for(parent)
