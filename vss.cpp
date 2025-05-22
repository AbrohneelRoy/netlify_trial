import java.util.*;

class Innings{
    private String bt;
    private Long runs;
    void get(String i1,long i2){
        this.bt=i1;
        this.runs=i2;
    }
    void set(){
            System.out.println("BattingTeam : "+bt);
            System.out.print("Run scored : "+runs);
        
    }
    
}
class main{
    public static void main(String args[]){
        Scanner s=new Scanner(System.in);
        Innings[] o=new Innings[2];
        for(int i=0; i<2; i++){
            o[i]=new Innings();
            String a=s.nextLine();
            long b=s.nextLong();
            o[i].get(a,b);
            s.nextLine();
        }
        for(int i=0; i<2; i++){
            System.out.print("Innings "+(i+1)+" Details\n");
            o[i].set();
        }
        
    }
}
