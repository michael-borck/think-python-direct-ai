"""
Project: Todo Application with GUI

Extracted from the companion book.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

class TodoGUI:
    """Main GUI application for Todo Manager"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("📋 Todo Manager")
        self.root.geometry("700x600")
        
        # Initialize task manager
        self.task_manager = TaskManager()
        self.selected_task_id: Optional[int] = None
        
        # Create interface
        self.create_widgets()
        self.refresh_task_display()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title and controls
        self.create_header(main_frame)
        
        # Add task section
        self.create_add_section(main_frame)
        
        # Task list section
        self.create_task_list(main_frame)
        
        # Control buttons
        self.create_controls(main_frame)
        
        # Statistics section
        self.create_statistics(main_frame)
    
    def create_header(self, parent):
        """Create header with title and file controls"""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, text="📋 Todo Manager", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # File controls
        file_frame = ttk.Frame(header_frame)
        file_frame.grid(row=0, column=1, sticky=tk.E)
        
        ttk.Button(file_frame, text="💾 Save", 
                  command=self.save_tasks).grid(row=0, column=0, padx=2)
        ttk.Button(file_frame, text="📁 Load", 
                  command=self.load_tasks).grid(row=0, column=1, padx=2)
        
        header_frame.columnconfigure(0, weight=1)
    
    def create_add_section(self, parent):
        """Create task addition section"""
        add_frame = ttk.LabelFrame(parent, text="Add New Task", padding="5")
        add_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        add_frame.columnconfigure(0, weight=1)
        
        # Task entry
        entry_frame = ttk.Frame(add_frame)
        entry_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        entry_frame.columnconfigure(0, weight=1)
        
        ttk.Label(entry_frame, text="Task:").grid(row=0, column=0, sticky=tk.W)
        self.task_entry = ttk.Entry(entry_frame, width=50)
        self.task_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 10))
        
        # Priority selection
        ttk.Label(entry_frame, text="Priority:").grid(row=0, column=2)
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(entry_frame, textvariable=self.priority_var,
                                     values=["High", "Medium", "Low"], 
                                     state="readonly", width=10)
        priority_combo.grid(row=0, column=3, padx=5)
        
        # Buttons
        button_frame = ttk.Frame(add_frame)
        button_frame.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        ttk.Button(button_frame, text="Add Task", 
                  command=self.add_task).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_entry).grid(row=0, column=1)
        
        # Bind Enter key to add task
        self.task_entry.bind('<Return>', lambda e: self.add_task())
    
    def create_task_list(self, parent):
        """Create task list display"""
        list_frame = ttk.LabelFrame(parent, text="Current Tasks", padding="5")
        list_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Task listbox with scrollbar
        listbox_frame = ttk.Frame(list_frame)
        listbox_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        listbox_frame.columnconfigure(0, weight=1)
        listbox_frame.rowconfigure(0, weight=1)
        
        self.task_listbox = tk.Listbox(listbox_frame, height=12, 
                                      font=('Courier', 10))
        self.task_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, 
                                 command=self.task_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        
        # Bind selection event
        self.task_listbox.bind('<<ListboxSelect>>', self.on_task_select)
    
    def create_controls(self, parent):
        """Create task control buttons"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Button(control_frame, text="✓ Complete Selected", 
                  command=self.complete_selected).grid(row=0, column=0, padx=2)
        ttk.Button(control_frame, text="○ Uncomplete Selected", 
                  command=self.uncomplete_selected).grid(row=0, column=1, padx=2)
        ttk.Button(control_frame, text="✏️ Edit Selected", 
                  command=self.edit_selected).grid(row=0, column=2, padx=2)
        ttk.Button(control_frame, text="🗑️ Delete Selected", 
                  command=self.delete_selected).grid(row=0, column=3, padx=2)
    
    def create_statistics(self, parent):
        """Create statistics display"""
        stats_frame = ttk.LabelFrame(parent, text="Statistics", padding="5")
        stats_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.stats_label = ttk.Label(stats_frame, text="No tasks yet")
        self.stats_label.grid(row=0, column=0, sticky=tk.W)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(stats_frame, variable=self.progress_var, 
                                          maximum=100, length=300)
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        stats_frame.columnconfigure(0, weight=1)
    
    def refresh_task_display(self):
        """Refresh the task list display"""
        # Clear current display
        self.task_listbox.delete(0, tk.END)
        
        # Add all tasks
        for task in self.task_manager.get_tasks():
            status = "✓" if task.completed else "○"
            priority_indicator = {
                "High": "🔴",
                "Medium": "🟡", 
                "Low": "🟢"
            }.get(task.priority, "⚪")
            
            display_text = f"{status} {priority_indicator} {task.priority.upper():<6} | {task.description}"
            self.task_listbox.insert(tk.END, display_text)
        
        # Update statistics
        self.update_statistics()
    
    def update_statistics(self):
        """Update statistics display"""
        stats = self.task_manager.get_statistics()
        
        stats_text = (f"📊 {stats['total']} total tasks | "
                     f"{stats['completed']} completed | "
                     f"{stats['remaining']} remaining")
        self.stats_label.config(text=stats_text)
        
        # Update progress bar
        self.progress_var.set(stats['completion_rate'])
    
    def add_task(self):
        """Add a new task"""
        description = self.task_entry.get().strip()
        if not description:
            messagebox.showwarning("Invalid Input", "Please enter a task description")
            return
        
        try:
            priority = self.priority_var.get()
            self.task_manager.add_task(description, priority)
            self.clear_entry()
            self.refresh_task_display()
            messagebox.showinfo("Success", f"Task added: {description}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add task: {e}")
    
    def clear_entry(self):
        """Clear the task entry field"""
        self.task_entry.delete(0, tk.END)
        self.priority_var.set("Medium")
        self.task_entry.focus()
    
    def on_task_select(self, event):
        """Handle task selection"""
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            tasks = self.task_manager.get_tasks()
            if 0 <= index < len(tasks):
                self.selected_task_id = tasks[index].id
    
    def complete_selected(self):
        """Mark selected task as complete"""
        if self.selected_task_id:
            if self.task_manager.complete_task(self.selected_task_id):
                self.refresh_task_display()
                messagebox.showinfo("Success", "Task marked as complete!")
    
    def uncomplete_selected(self):
        """Mark selected task as incomplete"""
        if self.selected_task_id:
            task = self.task_manager.get_task_by_id(self.selected_task_id)
            if task:
                task.uncomplete()
                self.task_manager.save_tasks()
                self.refresh_task_display()
                messagebox.showinfo("Success", "Task marked as incomplete!")
    
    def edit_selected(self):
        """Edit selected task"""
        if not self.selected_task_id:
            messagebox.showwarning("No Selection", "Please select a task to edit")
            return
        
        task = self.task_manager.get_task_by_id(self.selected_task_id)
        if not task:
            return
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Task")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, 
                                   self.root.winfo_rooty() + 50))
        
        # Edit form
        ttk.Label(dialog, text="Task Description:").pack(pady=5)
        
        edit_entry = ttk.Entry(dialog, width=50)
        edit_entry.pack(pady=5)
        edit_entry.insert(0, task.description)
        edit_entry.focus()
        
        ttk.Label(dialog, text="Priority:").pack(pady=5)
        
        priority_var = tk.StringVar(value=task.priority)
        priority_combo = ttk.Combobox(dialog, textvariable=priority_var,
                                     values=["High", "Medium", "Low"], 
                                     state="readonly")
        priority_combo.pack(pady=5)
        
        def save_edit():
            new_description = edit_entry.get().strip()
            if new_description:
                task.description = new_description
                task.priority = priority_var.get()
                self.task_manager.save_tasks()
                self.refresh_task_display()
                dialog.destroy()
                messagebox.showinfo("Success", "Task updated!")
            else:
                messagebox.showwarning("Invalid Input", "Description cannot be empty")
        
        def cancel_edit():
            dialog.destroy()
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Save", command=save_edit).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=cancel_edit).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to save
        edit_entry.bind('<Return>', lambda e: save_edit())
    
    def delete_selected(self):
        """Delete selected task"""
        if not self.selected_task_id:
            messagebox.showwarning("No Selection", "Please select a task to delete")
            return
        
        task = self.task_manager.get_task_by_id(self.selected_task_id)
        if not task:
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", 
                              f"Are you sure you want to delete:\n'{task.description}'?"):
            if self.task_manager.delete_task(self.selected_task_id):
                self.selected_task_id = None
                self.refresh_task_display()
                messagebox.showinfo("Success", "Task deleted!")
    
    def save_tasks(self):
        """Manually save tasks"""
        self.task_manager.save_tasks()
        messagebox.showinfo("Saved", "Tasks saved successfully!")
    
    def load_tasks(self):
        """Manually reload tasks"""
        self.task_manager.load_tasks()
        self.refresh_task_display()
        messagebox.showinfo("Loaded", "Tasks reloaded from file!")
    
    def on_closing(self):
        """Handle application closing"""
        # Auto-save before closing
        self.task_manager.save_tasks()
        self.root.destroy()

# Main application entry point
def main():
    """Run the Todo GUI application"""
    root = tk.Tk()
    app = TodoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
