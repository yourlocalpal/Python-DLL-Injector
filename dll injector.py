import ctypes
import tkinter as tk
from tkinter import filedialog


def inject_dll():
    # Get the target process ID and DLL file path from the user interface
    process_id = int(process_entry.get())
    dll_path = dll_entry.get()

    try:
        # Load the DLL file
        dll_handle = ctypes.WinDLL(dll_path)

        # Open the target process
        process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, process_id)

        if process_handle:
            # Allocate memory for the DLL path in the target process
            dll_path_address = ctypes.windll.kernel32.VirtualAllocEx(
                process_handle,
                0,
                len(dll_path),
                0x1000 | 0x2000,
                0x04,
            )

            if dll_path_address:
                # Write the DLL path to the allocated memory in the target process
                ctypes.windll.kernel32.WriteProcessMemory(
                    process_handle,
                    dll_path_address,
                    dll_path.encode("utf-8"),
                    len(dll_path),
                    None,
                )

                # Get the address of the LoadLibraryA function
                load_library_address = ctypes.windll.kernel32.GetProcAddress(
                    ctypes.windll.kernel32.GetModuleHandleA("kernel32.dll"),
                    "LoadLibraryA",
                )

                if load_library_address:
                    # Create a remote thread in the target process to load the DLL
                    ctypes.windll.kernel32.CreateRemoteThread(
                        process_handle,
                        None,
                        0,
                        load_library_address,
                        dll_path_address,
                        0,
                        None,
                    )

    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")
        return

    result_label.config(text="DLL injected successfully!")


def browse_dll_file():
    file_path = filedialog.askopenfilename(filetypes=[("Dynamic Link Library", "*.dll")])
    dll_entry.delete(0, tk.END)
    dll_entry.insert(0, file_path)


# Create the main window
window = tk.Tk()
window.title("Python DLL Injector")

# Create and place the process ID label and entry fields
process_label = tk.Label(window, text="Target Process ID:")
process_label.pack()
process_entry = tk.Entry(window)
process_entry.pack()

# Create and place the DLL file label, entry field, and browse button
dll_label = tk.Label(window, text="DLL File:")
dll_label.pack()
dll_entry = tk.Entry(window)
dll_entry.pack(side=tk.LEFT)
browse_button = tk.Button(window, text="Browse", command=browse_dll_file)
browse_button.pack(side=tk.RIGHT)

# Create and place the inject button
inject_button = tk.Button(window, text="Inject DLL", command=inject_dll)
inject_button.pack()

# Create and place the result label
result_label = tk.Label(window, text="")
result_label.pack()

# Start the GUI event loop
window.mainloop()
