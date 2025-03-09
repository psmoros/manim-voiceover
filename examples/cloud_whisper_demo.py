from manim import *
from manim_voiceover.voiceover_scene import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from manim_voiceover.services.recorder import RecorderService

class CloudWhisperDemo(VoiceoverScene):
    def construct(self):
        # Initialize speech service with cloud whisper option
        # Note: You can also run this with --use-cloud-whisper flag
        # instead of setting use_cloud_whisper=True here
        service = GTTSService(
            transcription_model="base",  # Model name is still required 
            use_cloud_whisper=True  # This enables cloud-based Whisper
        )
        self.set_speech_service(service)

        # Create a title
        title = Text("Cloud Whisper Demo", font_size=48)
        self.play(Write(title))
        self.wait()
        
        # Demonstrate voiceover with bookmarks
        with self.voiceover(
            """This demonstration uses <bookmark mark='cloud_point'/> cloud-based Whisper
            from OpenAI for speech-to-text <bookmark mark='alignment_point'/> alignment.
            """
        ) as tracker:
            # Wait until the first bookmark
            self.wait_until_bookmark("cloud_point")
            
            # Create and animate the cloud text
            cloud_text = Text("☁️ Cloud-based", color=BLUE, font_size=36)
            cloud_text.next_to(title, DOWN, buff=1)
            self.play(FadeIn(cloud_text))
            
            # Wait until the second bookmark
            self.wait_until_bookmark("alignment_point")
            
            # Create and animate the alignment text
            alignment_text = Text("Word-level Alignment", color=GREEN, font_size=36)
            alignment_text.next_to(cloud_text, DOWN, buff=0.5)
            self.play(FadeIn(alignment_text))
        
        # Continue with demonstration
        self.wait(1)
        
        # Show ARM64 compatibility
        arm_title = Text("Works on ARM64 Architectures!", color=YELLOW, font_size=36)
        arm_title.next_to(alignment_text, DOWN, buff=1)
        
        with self.voiceover(
            "This feature is especially useful for ARM64 architectures like Apple Silicon."
        ):
            self.play(FadeIn(arm_title))
        
        # Show how it's used
        self.wait(1)
        
        code_text = """
# Run with CLI flag:
manim -pql --use-cloud-whisper example.py MyScene

# Or enable programmatically:
service = GTTSService(
    transcription_model="base",
    use_cloud_whisper=True
)
        """
        code = Code(code=code_text, language="python", font_size=24)
        code.next_to(arm_title, DOWN, buff=1)
        
        with self.voiceover(
            "You can enable cloud-based Whisper using either a command-line flag or programmatically in your code."
        ):
            self.play(Create(code))
        
        self.wait(2)
        
        with self.voiceover(
            "This means you can use word-level alignment on any system without installing large local models."
        ):
            self.play(FadeOut(code, title, cloud_text, alignment_text, arm_title))
            
            final_text = Text("No Local Models Required!", font_size=48, color=BLUE)
            self.play(Write(final_text))
        
        self.wait(2) 