#Main function used to test
def main():
	#Keep in mind, python flips the bit's index
	#There's actually a different here
	print "Hello"
	print "Testing With AVVs 0000 and 0000"
	print unsignedsub_4bit(['0','0','0','0'],['0','0','0','0'])
	print "\n"
	
	print "Testing With AVVs 1111 and 1111"
	print unsignedsub_4bit(['1','1','1','1'],['1','1','1','1'])
	print "\n"

	print "Testing With AVVs 0101 and 1010"
	print unsignedsub_4bit(['1','0','1','0'],['0','1','0','1'])
	print "\n"

	print "Testing With AVVs 0110 and 0010"
	print unsignedsub_4bit(['0','1','1','0'],['0','1','0','0'])
	print "\n"

	print "Testing With AVVs TTTT and TTTT"
	print unsignedsub_4bit(['T','T','T','T'],['T','T','T','T'])
	print "\n"

	print "Testing With AVVs 0TT0 and T101"
	print unsignedsub_4bit(['0','T','T','0'],['1','0','1','T'])
	print "\n"

	print "Testing With AVVs 00T0 and 1101"
	print unsignedsub_4bit(['0','T','0','0'],['1','0','1','0'])
	print "\n"



#Takes in an abstract value vector and returns it's two's complement
#Inputs:
#	avv_convert - abstract value vector of arbitrary length
#Outputs:
#	avv_convert - twos complemented avv
def convert_twos_complement(avv_convert):
	for i in range(len(avv_convert)):
  		if avv_convert[i] == '1':
  			avv_convert[i] = '0';
		elif avv_convert[i] == 'T':
			avv_convert[i] = 'T';
		else:
			avv_convert[i] = '1';
	overflow = 1;
	for i in range(len(avv_convert)):
		if(overflow == -1 and avv_convert[i] == '0'):
			avv_convert[i] = 'T';
			overflow = 0;
		elif(overflow == -1 and avv_convert[i] != '0'):
			avv_convert[i] = 'T';
			overflow = -1;
		elif(overflow != -1 and avv_convert[i] != 'T'):
			temp = int(avv_convert[i],2) + overflow;
			overflow = (temp >> 1) & 1;	
			avv_convert[i] = str(temp & 1);
		elif(overflow == 1 and avv_convert[i] == 'T'):
			overflow =  -1;
	return avv_convert



#Abstract transfer function for unsigned addition
#This function assumes that the four bits are unsigned, and thus calculates two's complement by
#calculating the fifth sign bit. Though it does not return that bit in the result.
#This function takes in 4 bit abstract value vectors, and returns one as a result. Each AVV contains
#a number of abstract value bits, which can be '0', '1', or "unknown", which I represent with a 'T'.
#Inputs:
#	4bavv_minuend - 4 bit abstract value vector representing the left-hand side of the subtraction
#	4bavv_subtrahend -  4 bit abstract value vector representing the right-hand side of the subtraction
#Outputs:
#	avv_result - 4 bit abstract value vector representing the most precise result of the function
def unsignedsub_4bit(avv_minuend, avv_subtrahend):
	#Prepend zero since these are by definition unsigned
	bavv_minuend = avv_minuend + ['0'];
	bavv_subtrahend = avv_subtrahend + ['0'];

	#Convert the subtrahend so that we can compare via simple addition
	bavv_subtrahend = convert_twos_complement(bavv_subtrahend);
	print bavv_subtrahend

	#Create a transfer function matrix
	#matrix[ovf][min][sub]
	tfm_matrix = [
			[['T', 'T', 'T'], ['T', 'T', 'T'], ['T', 'T', 'T']], 
			[['T', 'T', 'T'], ['T', '0', '1'], ['T', '1', '0']], 
			[['T', 'T', 'T'], ['T', '1', '0'], ['T', '0', '1']]
		     ];
	#Create an overflow matrix 
	#matrix[ovf][min][sub]
	tfm_ovfmatrix = [
				[['T', 'T', 'T'], ['T', '0', 'T'], ['T', '0', 'T']], 
				[['T', '0', 'T'], ['0', '0', '0'], ['T', '0', '1']], 
				[['T', 'T', 'T'], ['T', '0', '1'], ['T', '1', '1']]
			];

	#Map the possible abstract bit values to an index into the transfer function matrix
	#1=2,0=1,T=0
	Avvmm_dict = {'T':0, '0':1, '1':2};

	#Calculate first bit (remember that 0 = index 1)
	avv_result = ['0', '0', '0', '0'];
	avv_result[0] = tfm_matrix[1] \
		[ Avvmm_dict[bavv_minuend[0]] ] \
		[ Avvmm_dict[bavv_subtrahend[0]] ];
	overflow = tfm_ovfmatrix[1] \
		[ Avvmm_dict[bavv_minuend[0]] ] \
		[ Avvmm_dict[bavv_subtrahend[0]] ];

	#Calculate second bit
	avv_result[1] = tfm_matrix[ Avvmm_dict[overflow] ] \
		[ Avvmm_dict[bavv_minuend[1]] ] \
		[ Avvmm_dict[bavv_subtrahend[1]] ];
	overflow = tfm_ovfmatrix[ Avvmm_dict[overflow] ] \
		[ Avvmm_dict[bavv_minuend[1]] ] \
		[ Avvmm_dict[bavv_subtrahend[1]] ];

	#Calculate Third bit
	avv_result[2] = tfm_matrix[ Avvmm_dict[overflow] ] \
		[ Avvmm_dict[bavv_minuend[2]] ] \
		[ Avvmm_dict[bavv_subtrahend[2]] ];
	overflow = tfm_ovfmatrix[ Avvmm_dict[overflow] ] \
		[ Avvmm_dict[bavv_minuend[2]] ] \
		[ Avvmm_dict[bavv_subtrahend[2]] ];

	#Calculate Fourth bit
	avv_result[3] = tfm_matrix[ Avvmm_dict[overflow] ] \
		[ Avvmm_dict[bavv_minuend[3]] ] \
		[ Avvmm_dict[bavv_subtrahend[3]] ];
	overflow = tfm_ovfmatrix[ Avvmm_dict[overflow] ] \
		[ Avvmm_dict[bavv_minuend[3]] ] \
		[ Avvmm_dict[bavv_subtrahend[3]] ];

	return avv_result;

if __name__ == "__main__":
	main()
