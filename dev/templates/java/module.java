package com.nanum.exobrain.search.etri;

public class module {
//객체변수 작성
/*
	private PrimarySearchFAQ faqIR;
*/
	public module(){
		try{
//로딩 작성
/*
		faqIR = new PrimarySearchFAQ("rscpath");
		System.out.println("PSFAQ IS LOADED");
*/
		} catch (Exception ex) {
		}
	}
	
	public String QA(String input){
//입출력 작성
/*
		try{

	    faqIR.readAnsUnit(input + "||0||{}");
        faqIR.do_primarySearch();
        output = faqIR.writeAnsUnit();
*/
		} catch (Exception ex) {
		}
		return output;

	}
}
