 # =Setup=
do_assembling = False
dictionary_instructions = {
    #1 = uses 8 bits, 2 = uses 16 bits, 3 = no hex. 
   "ld a, $": (0x3E, 1),
   "ld b, $": (0x06, 1),
   "ld c, $": (0x0E, 1),
   "ld d, $": (0x16, 1),
   "ld e, $": (0x1E, 1),
   "ld h, $": (0x26, 1),
   "ld l, $": (0x2E, 1),
   "ld ($), a": (0xEA, 2),
   "ld a, ($)": (0xFA, 2),
   "add a, $": (0xC6, 1),
   "sub a, $": (0xD6, 1),
   "adc a, $": (0xCE, 1),
   "sbc a, $": (0xDE, 1),
   "ld a, b": (0x78, 3),
   "ld b, a": (0x47, 3),
   "add a, b": (0x80, 3)
}
bin_file = []

 # =Actual execution code=
print("Enter folder directory")
directory = input("> ")
print("Directory is: ", directory)
print()
print("Enter code's filename")
filename = input("> ")
print("Filename is: ", filename)

file_place = str(directory + "\\" + filename)

try:
    with open(file_place, "r") as file:
         asm_code = file.read()
         asm_code_lines = asm_code.splitlines()
         do_assembling = True
except FileNotFoundError:
    print()
    print("ERROR: there is no file named:")
    print("\"" + file_place + "\"")
    print("Did you make a typo or something? if not, how do you forget if you put your file in the folder?")
    print()
    print("Program seized")
    raise SystemExit
          
if do_assembling:
          rom_adress = 0
          for i in range(len(asm_code_lines)):
              #First pass
              #awuip4zgsuivreilsyhçsgyuoidhjf
              current_line = asm_code_lines[i]
              if current_line.endswith(":"):
                  nametags[current_line.replace(":","")] = rom_adress
              else:
                  hex_start = -3
                  hex_end = -4
                  for asdfghjhgfds in range(len(current_line)):
                      if "$" in current_line[asdfghjhgfds] and hex_start < 0:
                          hex_start = asdfghjhgfds + 1
                      elif "$" in current_line[asdfghjhgfds] and hex_start >= 0:
                          print("ERROR: extra hex value on line " + str(i + 1) + ":")
                          print(current_line)
                          print("sorry, you can't add two hex values in one line! it is what it is.")
                          print()
                          print("Program siezed")
                          raise SystemExit
                      elif current_line[asdfghjhgfds] not in "0123456789ABCDEFabcdef" and hex_start >= 0 and hex_end < 0:
                           hex_end = asdfghjhgfds
                  if hex_start >= 0:
                      if hex_end < 0: #this should set the end of the hex to the last value of current_line if there is no letter after the last letter of the end of the hex value. i pray to god this works
                          hex_end = len(current_line)
                      hex_value = current_line[hex_start:hex_end]
                      instruction = current_line.replace(hex_value, "")
                  else:
                      instruction = current_line
                  if not instruction in dictionary_instructions:
                       print("ERROR: invalid instruction on line " + str(i + 1) + ":")
                       print(current_line)
                       print("This instruction is not valid on standard SM83 assembly. maybe you did a typo?")
                       print()
                       print("Program siezed")
                   else:
                       rom_adress = rom_adress + dictionary_instructions[instruction][2]            
          for i in range(len(asm_code_lines)):
              #Second pass
              current_line = asm_code_lines[i]
              hex_value_position = ""
              if not current_line == "":
                   divided_line = current_line.split(" ")
                   for j in range(len(divided_line)):
                       current_part = divided_line[j]
                       if current_part.startswith(("$","($")):
                           if hex_value_position == "":
                               thingy = current_part.find("$") #idk what should i name this variable
                               hex_value_position = j
                           else:
                               print("ERROR: extra hex value on line " + str(i + 1) + ":")
                               print(current_line)
                               print("sorry, you can't add two hex values in one line! it is what it is.")
                               print()
                               print("Program siezed")
                               raise SystemExit
                           try:
                               hex_value = int(current_part[thingy + 1:].replace(")","").replace(",",""), 16) #True + 1 = 2 because python interprets True as 1. or that's what i think.
                           except ValueError:
                               print("ERROR: invalid hex value on line " + str(i + 1) + ":")
                               print(current_line)
                               print("that ain't a hex value!")
                               print()
                               print("Program siezed")
                               raise SystemExit
                   final_line = divided_line.copy()
                   if not hex_value_position == "":
                       final_line[hex_value_position] = final_line[hex_value_position].translate(str.maketrans("", "", "0123456789ABCDEFabcdef")) #This should replace every instance of "0123456789ABCDEF" with "".
                   final_line_string = " ".join(final_line)
                   if not final_line_string in dictionary_instructions:
                       print("ERROR: invalid instruction on line " + str(i + 1) + ":")
                       print(current_line)
                       print("This instruction is not valid on standard SM83 assembly. maybe you did a typo?")
                       print()
                       print("Program siezed")
                   else:
                       opcode = dictionary_instructions[final_line_string][0]
                       bin_file.append(opcode)
                   if dictionary_instructions[final_line_string][1] == 2:
                       loby = hex_value & 0xFF
                       hiby = (hex_value >> 8)& 0xFF
                       bin_file.append(loby)
                       bin_file.append(hiby)
                   elif dictionary_instructions[final_line_string][1] == 1:
                       bin_file.append(hex_value)
                   else:
                       blip = "bloop"
                       pass
          print(bin_file)
          output_dir = str(directory + "\\" + "code.bin")
          with open(output_dir, "wb") as file:
              file.write(bytes(bin_file))
#FUCK DEBUGGING I HATE THAT SHIT
