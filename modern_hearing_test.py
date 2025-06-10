import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pygame
import threading
import time
import math
import traceback
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class ModernHearingTest:
    def __init__(self, master):
        try:
            print("Initializing Modern Hearing Test...")
            self.master = master
            master.title("🎵 Professional Hearing Test - Extended Range")
            master.geometry("900x750")
            master.configure(bg='#f0f0f0')
            
            # Initialize pygame
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
            
            # Variables
            self.freq_var = tk.DoubleVar(value=1000)
            self.volume_var = tk.DoubleVar(value=50)
            self.test_results = []
            self.manual_playing = False
            self.current_sound = None
            
            # Center window
            master.update_idletasks()
            x = (master.winfo_screenwidth() // 2) - 450
            y = (master.winfo_screenheight() // 2) - 375
            master.geometry(f"900x750+{x}+{y}")
            
            self.setup_ui()
            print("Modern UI setup complete!")
            
        except Exception as e:
            print(f"ERROR: {e}")
            traceback.print_exc()
    
    def setup_ui(self):
        # Main title
        title_frame = tk.Frame(self.master, bg='#f0f0f0', pady=15)
        title_frame.pack(fill=tk.X)
        
        title = tk.Label(title_frame, text="🎵 Professional Hearing Test", 
                        font=('Segoe UI', 20, 'bold'), bg='#f0f0f0', fg='#2c3e50')
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Extended Frequency Range: 10Hz - 28kHz", 
                           font=('Segoe UI', 12), bg='#f0f0f0', fg='#7f8c8d')
        subtitle.pack()
        
        # Control panel
        control_frame = tk.LabelFrame(self.master, text="🎛️ Test Controls", 
                                     font=('Segoe UI', 12, 'bold'), 
                                     bg='#f0f0f0', fg='#2c3e50', pady=10)
        control_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Frequency control
        freq_frame = tk.Frame(control_frame, bg='#f0f0f0')
        freq_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(freq_frame, text="🎚️ Frequency:", font=('Segoe UI', 11, 'bold'), 
                bg='#f0f0f0').pack(side=tk.LEFT)
        
        self.freq_slider = tk.Scale(freq_frame, from_=10, to=28000, 
                                   variable=self.freq_var, orient=tk.HORIZONTAL,
                                   length=400, font=('Segoe UI', 10),
                                   bg='#f0f0f0', fg='#2c3e50',
                                   command=self.on_freq_change)
        self.freq_slider.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.freq_display = tk.Label(freq_frame, text="1000 Hz", 
                                    font=('Segoe UI', 12, 'bold'), 
                                    fg='#e74c3c', bg='#f0f0f0', width=12)
        self.freq_display.pack(side=tk.RIGHT)
        
        # Volume control
        vol_frame = tk.Frame(control_frame, bg='#f0f0f0')
        vol_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(vol_frame, text="🔊 Volume:", font=('Segoe UI', 11, 'bold'), 
                bg='#f0f0f0').pack(side=tk.LEFT)
        
        vol_slider = tk.Scale(vol_frame, from_=0, to=100, 
                             variable=self.volume_var, orient=tk.HORIZONTAL,
                             length=400, font=('Segoe UI', 10),
                             bg='#f0f0f0', fg='#2c3e50')
        vol_slider.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        self.vol_display = tk.Label(vol_frame, text="50%", 
                                   font=('Segoe UI', 12, 'bold'), 
                                   fg='#3498db', bg='#f0f0f0', width=12)
        self.vol_display.pack(side=tk.RIGHT)
        
        # Control buttons
        btn_frame = tk.Frame(control_frame, bg='#f0f0f0')
        btn_frame.pack(pady=15)
        
        self.play_btn = tk.Button(btn_frame, text="🎵 PLAY TONE", 
                                 command=self.play_tone,
                                 bg='#27ae60', fg='white', 
                                 font=('Segoe UI', 12, 'bold'),
                                 width=15, height=2, relief=tk.FLAT, 
                                 cursor='hand2')
        self.play_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(btn_frame, text="⏹️ STOP", 
                                 command=self.stop_tone,
                                 bg='#e74c3c', fg='white', 
                                 font=('Segoe UI', 12, 'bold'),
                                 width=15, height=2, relief=tk.FLAT, 
                                 cursor='hand2', state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        # Frequency scale visualization
        self.setup_frequency_scale()
        
        # Response buttons
        self.setup_response_buttons()
        
        # Quick test frequencies
        self.setup_quick_frequencies()
        
        # Status
        self.status = tk.Label(self.master, text="🎯 Ready for testing", 
                              font=('Segoe UI', 12), fg='#27ae60', bg='#f0f0f0')
        self.status.pack(pady=10)
    
    def setup_frequency_scale(self):
        scale_frame = tk.LabelFrame(self.master, text="📊 Frequency Scale (10Hz - 28kHz)", 
                                   font=('Segoe UI', 12, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50')
        scale_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.canvas = tk.Canvas(scale_frame, width=800, height=100, 
                               bg='#ffffff', relief=tk.FLAT, bd=1)
        self.canvas.pack(pady=10)
        
        self.draw_scale()
        
        # Current frequency display
        self.current_freq_label = tk.Label(scale_frame, text="🎯 Current: 1000 Hz", 
                                          font=('Segoe UI', 14, 'bold'), 
                                          bg='#f0f0f0', fg='#2c3e50')
        self.current_freq_label.pack(pady=5)
    
    def setup_response_buttons(self):
        response_frame = tk.Frame(self.master, bg='#f0f0f0')
        response_frame.pack(fill=tk.X, padx=20, pady=15)
        
        # Can't hear button (left)
        self.cant_hear_btn = tk.Button(response_frame, 
                                      text="🚫 NIE SŁYSZĘ\nCan't Hear", 
                                      command=self.mark_not_heard,
                                      bg='#e74c3c', fg='white', 
                                      font=('Segoe UI', 13, 'bold'),
                                      width=18, height=3, relief=tk.FLAT, 
                                      cursor='hand2')
        self.cant_hear_btn.pack(side=tk.LEFT, padx=(0, 50))
        
        # Can hear button (right)
        self.can_hear_btn = tk.Button(response_frame, 
                                     text="✅ SŁYSZĘ\nCan Hear", 
                                     command=self.mark_heard,
                                     bg='#27ae60', fg='white', 
                                     font=('Segoe UI', 13, 'bold'),
                                     width=18, height=3, relief=tk.FLAT, 
                                     cursor='hand2')
        self.can_hear_btn.pack(side=tk.RIGHT, padx=(50, 0))
        
        # Report button (center)
        self.report_btn = tk.Button(response_frame, 
                                   text="📊 GENERATE REPORT\nCreate PDF", 
                                   command=self.generate_report,
                                   bg='#3498db', fg='white', 
                                   font=('Segoe UI', 12, 'bold'),
                                   width=20, height=2, relief=tk.FLAT, 
                                   cursor='hand2')
        self.report_btn.pack(pady=(20, 0))
    
    def setup_quick_frequencies(self):
        quick_frame = tk.LabelFrame(self.master, text="⚡ Quick Test Frequencies", 
                                   font=('Segoe UI', 12, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50')
        quick_frame.pack(fill=tk.X, padx=20, pady=10)
        
        freq_list = [20, 100, 250, 500, 1000, 2000, 4000, 8000, 16000]
        colors = ['#9b59b6', '#3498db', '#2ecc71', '#2ecc71', '#2ecc71', 
                 '#f39c12', '#f39c12', '#e74c3c', '#e74c3c']
        
        btn_frame = tk.Frame(quick_frame, bg='#f0f0f0')
        btn_frame.pack(pady=10)
        
        for i, (freq, color) in enumerate(zip(freq_list, colors)):
            if freq < 1000:
                text = f"{freq}Hz"
            else:
                text = f"{freq//1000}kHz"
                
            btn = tk.Button(btn_frame, text=text,
                           command=lambda f=freq: self.quick_test(f),
                           bg=color, fg='white', 
                           font=('Segoe UI', 10, 'bold'),
                           width=8, height=2, relief=tk.FLAT, cursor='hand2')
            btn.grid(row=0, column=i, padx=3, pady=2)
    
    def draw_scale(self):
        self.canvas.delete("all")
        
        # Draw scale line
        y_center = 50
        margin = 50
        width = 700
        
        self.canvas.create_line(margin, y_center, margin + width, y_center, 
                               width=4, fill='#2c3e50', capstyle=tk.ROUND)
        
        # Draw frequency markers
        frequencies = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 28000]
        
        for freq in frequencies:
            log_pos = (math.log10(freq) - math.log10(10)) / (math.log10(28000) - math.log10(10))
            x = margin + log_pos * width
            
            # Draw tick
            self.canvas.create_line(x, y_center - 10, x, y_center + 10, 
                                   width=2, fill='#34495e')
            
            # Label
            if freq < 1000:
                label = f"{freq}"
            else:
                label = f"{freq//1000}k"
            
            self.canvas.create_text(x, y_center - 20, text=label, 
                                   font=('Segoe UI', 9, 'bold'), fill='#34495e')
    
    def on_freq_change(self, value):
        freq = int(float(value))
        if freq < 1000:
            self.freq_display.config(text=f"{freq} Hz")
            self.current_freq_label.config(text=f"🎯 Current: {freq} Hz")
        else:
            self.freq_display.config(text=f"{freq/1000:.1f} kHz")
            self.current_freq_label.config(text=f"🎯 Current: {freq/1000:.1f} kHz")
        
        # Update indicator on scale
        self.update_indicator(freq)
        
        if self.manual_playing:
            self.stop_tone()
            self.play_tone()
    
    def update_indicator(self, freq):
        # Remove old indicator
        self.canvas.delete("indicator")
        
        # Calculate position
        margin = 50
        width = 700
        y_center = 50
        
        if 10 <= freq <= 28000:
            log_pos = (math.log10(freq) - math.log10(10)) / (math.log10(28000) - math.log10(10))
            x = margin + log_pos * width
            
            # Draw indicator
            self.canvas.create_line(x, y_center - 15, x, y_center + 15, 
                                   width=4, fill='#e74c3c', tags="indicator")
            self.canvas.create_oval(x-6, y_center-20, x+6, y_center-8, 
                                   fill='#e74c3c', tags="indicator")
    
    def generate_tone(self, freq, duration=5.0):
        try:
            t = np.linspace(0, duration, int(duration * 44100), False)
            tone = np.sin(2 * np.pi * freq * t)
            volume = self.volume_var.get() / 100.0
            tone = tone * volume * 0.3
            tone = (tone * 32767).astype(np.int16)
            stereo_tone = np.column_stack((tone, tone))
            return stereo_tone
        except Exception as e:
            print(f"Error generating tone: {e}")
            return None
    
    def play_tone(self):
        try:
            if self.manual_playing:
                return
                
            freq = int(self.freq_var.get())
            self.manual_playing = True
            
            self.play_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.status.config(text=f"🎵 Playing {freq} Hz tone...", fg='#3498db')
            
            tone_data = self.generate_tone(freq)
            if tone_data is not None:
                sound = pygame.sndarray.make_sound(tone_data)
                sound.play(-1)
                self.current_sound = sound
                
        except Exception as e:
            print(f"Error playing tone: {e}")
            self.stop_tone()
    
    def stop_tone(self):
        try:
            self.manual_playing = False
            pygame.mixer.stop()
            self.current_sound = None
            
            self.play_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.status.config(text="🎯 Ready for testing", fg='#27ae60')
            
        except Exception as e:
            print(f"Error stopping tone: {e}")
    
    def quick_test(self, freq):
        self.freq_var.set(freq)
        self.on_freq_change(freq)
        self.play_tone()
    
    def mark_heard(self):
        freq = int(self.freq_var.get())
        vol = int(self.volume_var.get())
        
        result = {
            'frequency': freq,
            'volume': vol,
            'heard': True,
            'timestamp': datetime.now()
        }
        self.test_results.append(result)
        
        self.status.config(text=f"✅ {freq} Hz - SŁYSZĘ (Volume: {vol}%)", fg='#27ae60')
        self.stop_tone()
    
    def mark_not_heard(self):
        freq = int(self.freq_var.get())
        vol = int(self.volume_var.get())
        
        result = {
            'frequency': freq,
            'volume': vol,
            'heard': False,
            'timestamp': datetime.now()
        }
        self.test_results.append(result)
        
        self.status.config(text=f"🚫 {freq} Hz - NIE SŁYSZĘ (Volume: {vol}%)", fg='#e74c3c')
        self.stop_tone()
    
    def generate_report(self):
        if not self.test_results:
            messagebox.showwarning("No Data", "Please complete some hearing tests first!")
            return
        
        try:
            filename = f"hearing_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            doc = SimpleDocTemplate(filename, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            story.append(Paragraph("🎵 HEARING TEST REPORT", styles['Title']))
            story.append(Spacer(1, 12))
            
            # Summary
            heard_count = sum(1 for r in self.test_results if r['heard'])
            total_tests = len(self.test_results)
            success_rate = (heard_count / total_tests * 100) if total_tests > 0 else 0
            
            story.append(Paragraph(f"Total Tests: {total_tests}", styles['Normal']))
            story.append(Paragraph(f"Frequencies Heard: {heard_count}", styles['Normal']))
            story.append(Paragraph(f"Success Rate: {success_rate:.1f}%", styles['Normal']))
            story.append(Spacer(1, 20))
            
            # Results table
            table_data = [['Frequency (Hz)', 'Volume (%)', 'Result', 'Time']]
            
            for result in sorted(self.test_results, key=lambda x: x['frequency']):
                table_data.append([
                    str(result['frequency']),
                    str(result['volume']),
                    'HEARD ✓' if result['heard'] else 'NOT HEARD ✗',
                    result['timestamp'].strftime('%H:%M:%S')
                ])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            story.append(table)
            doc.build(story)
            
            messagebox.showinfo("Report Generated", f"Report saved as: {filename}")
            self.status.config(text=f"📊 Report generated: {filename}", fg='#3498db')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

def main():
    try:
        print("Creating Modern Hearing Test...")
        root = tk.Tk()
        app = ModernHearingTest(root)
        
        # Make sure window is visible
        root.lift()
        root.attributes('-topmost', True)
        root.update()
        root.attributes('-topmost', False)
        root.focus_force()
        
        def on_closing():
            try:
                if app.manual_playing:
                    app.stop_tone()
                pygame.mixer.quit()
                root.destroy()
            except:
                pass
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        print("✅ MODERN HEARING TEST IS RUNNING!")
        print("Window should be visible now - check Alt+Tab if needed")
        
        root.mainloop()
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
