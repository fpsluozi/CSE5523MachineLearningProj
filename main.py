from buildFeaVec import BuildFeaVec 

def main():
	b = BuildFeaVec()
	b.build_feature_matrix("dataset/test.csv")

if __name__ == '__main__':
	main()