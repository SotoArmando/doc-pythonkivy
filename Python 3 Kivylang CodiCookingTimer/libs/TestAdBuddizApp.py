from kivy.app import App
from kivy.uix.button import Button

from jnius import autoclass

from kivy.utils import platform

if platform=="android":
    PythonActivity=autoclass("org.renpy.android.PythonActivity")
    AdBuddiz=autoclass("com.purplebrain.adbuddiz.sdk.AdBuddiz")

class TestAdBuddizApp(App):
    def build(self):
        return Button(text="Show ads", on_release=self.show_ads)
    def on_start(self):
        AdBuddiz.setPublisherKey("TEST_PUBLISHER_KEY") #replace with the key of your app
        AdBuddiz.setTestModeActive()
        AdBuddiz.cacheAds(PythonActivity.mActivity)
    def on_pause(self):
    	return True
    def on_resume(self):
    	pass
    def show_ads(*args):
        AdBuddiz.showAd(PythonActivity.mActivity)

if __name__=="__main__":
    TestAdBuddizApp().run()