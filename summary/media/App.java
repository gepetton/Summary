package com.postgresqltutorial;

import java.sql.*;


public class App {

	private final String url = "jdbc:postgresql://localhost:5432/postgres";
	private final String user = "choijin-won";
	private final String password = "5082";
	
	public static void main(String[] args) {
		App app = new App();
		Connection conn = app.connect();
		app.statementQueryEx1(conn);
		app.statementQueryEx2(conn);
		app.prepareStatementQueryEx1(conn);
		app.disconnect(conn);
	}
	
	public Connection connect() {
		Connection conn = null;
		try {
			conn = DriverManager.getConnection(url, user, password);
			System.out.println("Connected to the PostgreSQL server successfully.");
		} catch (SQLException e) {
			System.out.println(e.getMessage());
		}
		
		return conn;
	}
	
	public void statementQueryEx1(Connection conn) {
		System.out.println("========================");
		System.out.println("statementQueryEx1");
		System.out.println("========================");
		
		try {
			Statement st = conn.createStatement();
			ResultSet rs = st.executeQuery("SELECT count(*) FROM instructor");
			rs.next();
			int count = rs.getInt(1);
			
			System.out.println("number of instructor=" + count);
			rs.close();
			st.close();
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		System.out.println("");
		System.out.println("");
	}
	
	public void statementQueryEx2(Connection conn) {
		System.out.println("========================");
		System.out.println("statementQueryEx2");
		System.out.println("========================");
		
		try {
			Statement st = conn.createStatement();
			ResultSet rs = st.executeQuery("SELECT * FROM instructor");
			displayInstructor(rs);
			rs.close();
			st.close();
		} catch(SQLException e) {
			e.printStackTrace();
		}
		
		System.out.println("");
		System.out.println("");
	}
	
	public void prepareStatementQueryEx1(Connection conn) {
		System.out.println("========================");
		System.out.println("prepareStatementQueryEx1");
		System.out.println("========================");
		
		String SQL = "SELECT id, name, dept_name, salary "
				+ "FROM instructor "
				+ "WHERE id = ?";
		
		try {
			PreparedStatement pstmt = conn.prepareStatement(SQL);
			pstmt.setString(1, "22222");
			ResultSet rs = pstmt.executeQuery();
			displayInstructor(rs);
		} catch (SQLException e) {
			e.printStackTrace();
		}
		
		System.out.println("");
		System.out.println("");		
	}
	
	private void displayInstructor(ResultSet rs) throws SQLException {
		while(rs.next()) {
			System.out.println(rs.getString(1) + "\t"
					+ rs.getString(2) + "\t"
					+ rs.getString("dept_name") + "\t"
					+ rs.getBigDecimal("salary"));
		}
	}
	
	public void disconnect(Connection conn) {
		try {
			conn.close();
			System.out.println("Connection is closed successfully.");
		} catch (SQLException e) {
			System.out.println(e.getMessage());
		}
	}
}
